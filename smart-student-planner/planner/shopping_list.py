from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from planner.catalog import Ingredient, Recipe


@dataclass(frozen=True)
class ShoppingLine:
    ingredient: Ingredient
    needed: int
    from_pantry: int
    packages: int

    @property
    def missing(self) -> int:
        return self.needed - self.from_pantry

    @property
    def cost_agorot(self) -> int:
        return self.packages * self.ingredient.pack_price_agorot


@dataclass(frozen=True)
class ShoppingList:
    lines: tuple[ShoppingLine, ...]

    @property
    def total_agorot(self) -> int:
        return sum(line.cost_agorot for line in self.lines)


def price_basket(
    dinners: Iterable[Recipe],
    catalog: Mapping[str, Ingredient],
    pantry: Mapping[str, int],
) -> ShoppingList:
    needed: Counter[str] = Counter()
    for dinner in dinners:
        needed.update(dinner.ingredients)

    lines = []
    for ingredient_id in sorted(needed, key=lambda item: catalog[item].name):
        ingredient = catalog[ingredient_id]
        total_needed = needed[ingredient_id]
        from_pantry = min(total_needed, pantry.get(ingredient_id, 0))
        missing = total_needed - from_pantry
        # Round the missing amount up to whole packs using integer arithmetic.
        packages = (missing + ingredient.pack_size - 1) // ingredient.pack_size
        lines.append(ShoppingLine(ingredient, total_needed, from_pantry, packages))
    return ShoppingList(tuple(lines))
