import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Ingredient:
    name: str
    unit: str
    pack_size: int
    pack_price_agorot: int


@dataclass(frozen=True)
class Recipe:
    name: str
    ingredients: dict[str, int]
    steps: tuple[str, ...]


def load_ingredients(path: Path) -> dict[str, Ingredient]:
    ingredients: dict[str, Ingredient] = {}
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            ingredient_id = row["id"]
            ingredient = Ingredient(
                name=row["name"],
                unit=row["unit"],
                pack_size=int(row["pack_size"]),
                pack_price_agorot=int(row["pack_price_agorot"]),
            )
            if (
                not ingredient_id
                or ingredient_id in ingredients
                or not ingredient.name
                or ingredient.unit not in {"g", "ml", "piece"}
                or ingredient.pack_size <= 0
                or ingredient.pack_price_agorot < 0
            ):
                raise ValueError(f"Invalid or duplicate catalog row for {ingredient_id!r}.")
            ingredients[ingredient_id] = ingredient
    return dict(sorted(ingredients.items(), key=lambda item: item[1].name))


def load_recipes(path: Path, ingredients: dict[str, Ingredient]) -> tuple[Recipe, ...]:
    with path.open(encoding="utf-8") as file:
        rows = json.load(file)

    recipes = []
    for row in rows:
        name = row["name"]
        amounts = row["ingredients"]
        if not amounts or any(
            ingredient_id not in ingredients or type(amount) is not int or amount < 1
            for ingredient_id, amount in amounts.items()
        ):
            raise ValueError(f"{name!r} needs valid catalog ingredients and whole quantities.")
        recipes.append(Recipe(name=name, ingredients=amounts, steps=tuple(row["steps"])))
    return tuple(recipes)
