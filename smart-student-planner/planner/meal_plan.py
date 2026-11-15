from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from itertools import combinations

from planner.catalog import Ingredient, Recipe
from planner.shopping_list import ShoppingList, price_basket


@dataclass(frozen=True)
class MealPlan:
    dinners: tuple[Recipe, ...]
    shopping_list: ShoppingList
    budget_agorot: int

    @property
    def remaining_agorot(self) -> int:
        return self.budget_agorot - self.shopping_list.total_agorot


def find_plan(
    recipes: Iterable[Recipe],
    catalog: Mapping[str, Ingredient],
    pantry: Mapping[str, int],
    budget_agorot: int,
) -> MealPlan | None:
    best_plan = None
    for dinners in combinations(recipes, 3):
        shopping_list = price_basket(dinners, catalog, pantry)
        total = shopping_list.total_agorot
        if total > budget_agorot:
            continue
        # Keeping the first match makes equal-price results repeatable.
        if best_plan is None or total < best_plan.shopping_list.total_agorot:
            best_plan = MealPlan(dinners, shopping_list, budget_agorot)
    return best_plan
