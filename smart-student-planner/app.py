from pathlib import Path
import re

from flask import Flask, render_template, request

from planner.catalog import load_ingredients, load_recipes
from planner.meal_plan import find_plan


app = Flask(__name__)
DATA_DIR = Path(__file__).resolve().parent / "data"
INGREDIENTS = load_ingredients(DATA_DIR / "ingredients.csv")
RECIPES = load_recipes(DATA_DIR / "starter_recipes.json", INGREDIENTS)

SAMPLE_BUDGET = "30.00"
SAMPLE_PANTRY = [("rice", "200"), ("eggs", "4"), ("oil", "35")]
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


def parse_pantry(rows: list[tuple[str, str]]) -> dict[str, int]:
    pantry: dict[str, int] = {}
    for row_number, (ingredient_id, raw_amount) in enumerate(rows, start=1):
        if ingredient_id not in INGREDIENTS:
            raise ValueError(f"Choose an ingredient for pantry row {row_number}.")
        value = raw_amount.strip()
        try:
            amount = int(value) if value.isascii() and value.isdecimal() else 0
        except ValueError:
            amount = 0
        if amount < 1:
            raise ValueError(f"Enter a positive whole amount for pantry row {row_number}.")
        pantry[ingredient_id] = pantry.get(ingredient_id, 0) + amount
    return pantry


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
    is_sample = request.method == "GET"
    if is_sample:
        raw_budget = SAMPLE_BUDGET
        rows = SAMPLE_PANTRY
    else:
        raw_budget = request.form.get("budget", "")
        rows = [
            (request.form.get(f"ingredient_{number}", ""), request.form.get(f"amount_{number}", ""))
            for number in range(1, 4)
        ]

    context = {
        "raw_budget": raw_budget,
        "rows": rows,
        "ingredients": INGREDIENTS,
        "is_sample": is_sample,
    }
    try:
        budget = parse_budget(raw_budget)
        pantry = parse_pantry(rows)
    except ValueError as error:
        return render_template("index.html", **context, error=str(error)), 400

    plan = find_plan(RECIPES, INGREDIENTS, pantry, budget)
    return render_template("index.html", **context, budget=budget, plan=plan)


if __name__ == "__main__":
    app.run()
