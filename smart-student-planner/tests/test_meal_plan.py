from pathlib import Path
import unittest

from planner.catalog import Ingredient, Recipe, load_ingredients, load_recipes
from planner.meal_plan import find_plan


class MealPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_dir = Path(__file__).resolve().parents[1] / "data"
        cls.catalog = load_ingredients(data_dir / "ingredients.csv")
        cls.recipes = load_recipes(data_dir / "starter_recipes.json", cls.catalog)
        cls.pantry = {"rice": 200, "eggs": 4, "oil": 35}

    def test_sample_matches_the_hand_calculated_basket(self):
        plan = find_plan(self.recipes, self.catalog, self.pantry, 3000)

        self.assertIsNotNone(plan)
        self.assertEqual(len(plan.dinners), 3)
        self.assertEqual(plan.shopping_list.total_agorot, 2250)
        self.assertEqual(plan.remaining_agorot, 750)

    def test_accepts_a_basket_at_the_exact_budget(self):
        plan = find_plan(self.recipes, self.catalog, self.pantry, 2250)

        self.assertIsNotNone(plan)
        self.assertEqual(plan.remaining_agorot, 0)

    def test_reports_no_plan_below_the_lowest_cost(self):
        self.assertIsNone(find_plan(self.recipes, self.catalog, self.pantry, 2249))

    def test_optimizes_the_combined_basket(self):
        catalog = {
            "single": Ingredient("Single item", "piece", 1, 150),
            "bundle": Ingredient("Bundled item", "piece", 3, 300),
        }
        recipes = [
            Recipe("Single dinner", {"single": 1}, ()),
            Recipe("Stovetop single dinner", {"single": 1}, ()),
            Recipe("Baked single dinner", {"single": 1}, ()),
            Recipe("Bundle dinner", {"bundle": 1}, ()),
            Recipe("Stovetop bundle dinner", {"bundle": 1}, ()),
            Recipe("Baked bundle dinner", {"bundle": 1}, ()),
        ]

        plan = find_plan(recipes, catalog, {}, 500)

        self.assertIsNotNone(plan)
        self.assertEqual(plan.shopping_list.total_agorot, 300)
        self.assertTrue(all("bundle" in dinner.ingredients for dinner in plan.dinners))
