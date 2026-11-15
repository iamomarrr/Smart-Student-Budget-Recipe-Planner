import unittest

from planner.catalog import Ingredient, Recipe
from planner.shopping_list import price_basket


class ShoppingListTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {"rice": Ingredient("Rice", "g", 1000, 800)}

    def test_combines_meals_before_subtracting_pantry(self):
        dinners = [
            Recipe("Rice bowl", {"rice": 250}, ()),
            Recipe("Fried rice", {"rice": 250}, ()),
        ]
        basket = price_basket(dinners, self.catalog, {"rice": 200})

        (line,) = basket.lines
        self.assertEqual(line.needed, 500)
        self.assertEqual(line.from_pantry, 200)
        self.assertEqual(line.missing, 300)
        self.assertEqual(line.packages, 1)
        self.assertEqual(basket.total_agorot, 800)

    def test_counts_exact_number_of_full_packs(self):
        dinners = [Recipe("Rice dish", {"rice": 2100}, ())]
        basket = price_basket(dinners, self.catalog, {"rice": 100})

        (line,) = basket.lines
        self.assertEqual(line.packages, 2)
        self.assertEqual(basket.total_agorot, 1600)

    def test_pantry_coverage_costs_zero(self):
        dinners = [Recipe("Rice dish", {"rice": 150}, ())]
        basket = price_basket(dinners, self.catalog, {"rice": 200})

        (line,) = basket.lines
        self.assertEqual(line.from_pantry, 150)
        self.assertEqual(line.packages, 0)
        self.assertEqual(basket.total_agorot, 0)
