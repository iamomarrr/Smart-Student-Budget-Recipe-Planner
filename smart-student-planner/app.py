from collections.abc import Mapping
from pathlib import Path
import re

from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from ai.photo_ingredients import (
    MAX_PHOTO_BYTES,
    MAX_PHOTO_MB,
    PhotoAnalysisError,
    PhotoInputError,
    suggest_ingredients,
)
from planner.catalog import load_ingredients, load_recipes
from planner.meal_plan import find_plan


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_PHOTO_BYTES + 1024 * 1024
DATA_DIR = Path(__file__).resolve().parent / "data"
INGREDIENTS = load_ingredients(DATA_DIR / "ingredients.csv")
RECIPES = load_recipes(DATA_DIR / "starter_recipes.json", INGREDIENTS)

SAMPLE_BUDGET = "30.00"
SAMPLE_PANTRY = [("rice", "200"), ("eggs", "4"), ("oil", "35")]
INITIAL_PANTRY_ROWS = len(SAMPLE_PANTRY)
PANTRY_FIELD = re.compile(r"(?:ingredient|amount)_([1-9][0-9]*)")
BUDGET_FORMAT = re.compile(r"(?:[0-9]+(?:\.[0-9]{1,2})?|\.[0-9]{1,2})")


def parse_budget(value: str) -> int:
    """Return the amount in agorot, the hundredths of a shekel."""
    value = value.strip()
    if BUDGET_FORMAT.fullmatch(value) is None:
        raise ValueError("Enter a budget of 0 or more, with up to two decimal places.")
    shekels, _, agorot = value.partition(".")
    try:
        return int(shekels or "0") * 100 + int(agorot.ljust(2, "0"))
    except ValueError as error:
        raise ValueError("Enter a smaller budget.") from error


def read_pantry_rows(form: Mapping[str, str]) -> list[tuple[str, str]]:
    row_ids = {str(number) for number in range(1, INITIAL_PANTRY_ROWS + 1)}
    for field_name in form:
        match = PANTRY_FIELD.fullmatch(field_name)
        if match:
            row_ids.add(match[1])

    # Keep numeric order as the form grows past nine rows.
    ordered_ids = sorted(row_ids, key=lambda row_id: (len(row_id), row_id))
    return [
        (form.get(f"ingredient_{row_id}", ""), form.get(f"amount_{row_id}", ""))
        for row_id in ordered_ids
    ]


def parse_pantry(rows: list[tuple[str, str]]) -> dict[str, int]:
    pantry: dict[str, int] = {}
    for row_number, (ingredient_id, raw_amount) in enumerate(rows, start=1):
        value = raw_amount.strip()
        if not ingredient_id and not value:
            continue
        if ingredient_id not in INGREDIENTS:
            raise ValueError(f"Choose an ingredient for pantry row {row_number}.")
        try:
            amount = int(value) if value.isascii() and value.isdecimal() else 0
        except ValueError:
            amount = 0
        if amount < 1:
            raise ValueError(f"Enter a positive whole amount for pantry row {row_number}.")
        pantry[ingredient_id] = pantry.get(ingredient_id, 0) + amount
    return pantry


def form_context(
    raw_budget: str,
    rows: list[tuple[str, str]],
    *,
    is_sample: bool = False,
    is_blank: bool = False,
) -> dict:
    return {
        "raw_budget": raw_budget,
        "rows": rows,
        "ingredients": INGREDIENTS,
        "initial_pantry_rows": INITIAL_PANTRY_ROWS,
        "is_sample": is_sample,
        "is_blank": is_blank,
        "max_photo_mb": MAX_PHOTO_MB,
    }


@app.template_filter("money")
def format_money(agorot: int) -> str:
    shekels, remainder = divmod(agorot, 100)
    return f"NIS {shekels:,}.{remainder:02d}"


@app.template_filter("quantity")
def format_quantity(amount: int, unit: str) -> str:
    if unit == "piece" and amount != 1:
        unit = "pieces"
    return f"{amount:,} {unit}"


@app.route("/", methods=["GET", "POST"])
def index():
    is_post = request.method == "POST"
    is_blank = not is_post and request.args.get("blank") == "1"
    is_sample = not is_post and not is_blank
    if is_post:
        raw_budget = request.form.get("budget", "")
        rows = read_pantry_rows(request.form)
    elif is_blank:
        raw_budget = ""
        rows = [("", "")] * INITIAL_PANTRY_ROWS
    else:
        raw_budget = SAMPLE_BUDGET
        rows = SAMPLE_PANTRY.copy()

    context = form_context(raw_budget, rows, is_sample=is_sample, is_blank=is_blank)
    if is_blank:
        return render_template("index.html", **context)

    if is_post:
        if request.form.get("action") == "add_ingredient":
            rows.append(("", ""))
            return render_template("index.html", **context)
        if "remove_ingredient" in request.form:
            row_number = request.form.get("remove_ingredient", type=int)
            if row_number is None or not INITIAL_PANTRY_ROWS < row_number <= len(rows):
                return render_template(
                    "index.html", **context, error="Choose an extra pantry row to remove."
                ), 400
            rows.pop(row_number - 1)
            return render_template("index.html", **context)

    try:
        budget = parse_budget(raw_budget)
        pantry = parse_pantry(rows)
    except ValueError as error:
        return render_template("index.html", **context, error=str(error)), 400

    plan = find_plan(RECIPES, INGREDIENTS, pantry, budget)
    return render_template("index.html", **context, budget=budget, plan=plan)


@app.post("/photo")
def analyze_photo():
    rows = read_pantry_rows(request.form)
    context = form_context(request.form.get("budget", ""), rows)
    photo = request.files.get("photo")
    if not photo or not photo.filename:
        return render_template("index.html", **context, error="Choose a photo or screenshot first."), 400

    try:
        suggestions = suggest_ingredients(photo.stream.read(MAX_PHOTO_BYTES + 1), INGREDIENTS)
    except PhotoInputError as error:
        return render_template("index.html", **context, error=str(error)), 400
    except PhotoAnalysisError as error:
        return render_template("index.html", **context, error=str(error)), 503

    entered = {ingredient_id for ingredient_id, _ in rows}
    additions = [item for item in suggestions if item not in entered]
    blank_rows = [index for index, (item, amount) in enumerate(rows) if not item and not amount.strip()]
    for index, item in zip(blank_rows, additions):
        rows[index] = (item, "")
    rows.extend((item, "") for item in additions[len(blank_rows):])

    if additions:
        names = ", ".join(INGREDIENTS[item].name for item in additions)
        notice = f"Suggested {names}. Check the new rows and enter their amounts."
    elif suggestions:
        notice = "The suggested ingredients are already in your pantry list."
    else:
        notice = "No catalog ingredients were identified. Try a clearer image or add the items by hand."
    return render_template("index.html", **context, notice=notice)


@app.errorhandler(RequestEntityTooLarge)
def upload_too_large(_error):
    context = form_context("", [("", "")] * INITIAL_PANTRY_ROWS, is_blank=True)
    return render_template("index.html", **context, error=f"Choose an image up to {MAX_PHOTO_MB} MB."), 413


if __name__ == "__main__":
    app.run()
