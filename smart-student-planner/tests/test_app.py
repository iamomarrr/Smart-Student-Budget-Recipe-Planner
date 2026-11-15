from io import BytesIO
import os
import unittest
from unittest.mock import patch

from PIL import Image

from app import app


class FlaskDemoTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.form = {
            "budget": "30.00",
            "ingredient_1": "rice",
            "amount_1": "200",
            "ingredient_2": "eggs",
            "amount_2": "4",
            "ingredient_3": "oil",
            "amount_3": "35",
        }

    def test_home_page_loads_a_real_example(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NIS 22.50", response.data)
        self.assertIn(b"NIS 7.50", response.data)

    def test_submit_uses_the_new_budget(self):
        self.form["budget"] = "22.50"
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NIS 0.00", response.data)

    def test_submit_too_low_a_budget(self):
        self.form["budget"] = "22.49"
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No plan fits NIS 22.49", response.data)

    def test_invalid_budget_has_a_clear_message(self):
        self.form["budget"] = "23.495"
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"up to two decimal places", response.data)

    def test_invalid_pantry_amount_has_a_clear_message(self):
        self.form["amount_2"] = "-1"
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"positive whole amount for pantry row 2", response.data)

    def test_add_ingredient_twice_keeps_the_entered_values(self):
        form = dict(self.form, budget="27.00", amount_1="210", action="add_ingredient")
        first = self.client.post("/", data=form)
        form.update(ingredient_4="", amount_4="")
        second = self.client.post("/", data=form)

        self.assertEqual(first.status_code, 200)
        self.assertIn(b'name="ingredient_4"', first.data)
        self.assertNotIn(b'name="ingredient_5"', first.data)
        self.assertEqual(second.status_code, 200)
        self.assertIn(b'name="ingredient_4"', second.data)
        self.assertIn(b'name="ingredient_5"', second.data)
        self.assertIn(b'name="amount_5"', second.data)
        self.assertRegex(second.get_data(as_text=True), r'name="budget"[^>]*value="27\.00"')
        self.assertRegex(second.get_data(as_text=True), r'name="amount_1"[^>]*value="210"')

    def test_five_ingredients_change_the_shopping_list(self):
        self.form.update(ingredient_4="tomato", amount_4="3", ingredient_5="onion", amount_5="2")
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NIS 11.50", response.data)
        self.assertIn(b"NIS 18.50", response.data)
        shopping_table = response.data.split(b'<table class="shopping-table">', 1)[1].split(b"</table>", 1)[0]
        self.assertIn(b"Drained chickpeas", shopping_table)
        self.assertIn(b"Pasta", shopping_table)
        self.assertNotIn(b"Tomatoes", shopping_table)
        self.assertNotIn(b"Onions", shopping_table)

    def test_blank_extra_row_can_be_left_unused(self):
        self.form.update(ingredient_4="", amount_4="")
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NIS 22.50", response.data)

    def test_extra_ingredient_requires_a_quantity(self):
        self.form.update(ingredient_4="tomato", amount_4="")
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"positive whole amount for pantry row 4", response.data)

    def test_remove_accidental_blank_row(self):
        self.form.update(ingredient_4="", amount_4="", remove_ingredient="4")
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="ingredient_3"', response.data)
        self.assertNotIn(b'name="ingredient_4"', response.data)
        self.assertIn(b'value="30.00"', response.data)

    def test_remove_one_extra_row_keeps_the_other(self):
        self.form.update(
            ingredient_4="tomato", amount_4="3",
            ingredient_5="onion", amount_5="2",
            remove_ingredient="4",
        )
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'name="ingredient_5"', response.data)
        remaining_row = response.get_data(as_text=True).split('name="ingredient_4"', 1)[1]
        self.assertIn('<option value="onion" selected>', remaining_row.split("</select>", 1)[0])
        self.assertRegex(remaining_row, r'name="amount_4"[^>]*value="2"')

    def test_rejects_a_remove_request_for_a_starting_row(self):
        response = self.client.post("/", data=dict(self.form, remove_ingredient="1"))

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Choose an extra pantry row to remove.", response.data)

    def test_start_blank_clears_budget_and_pantry(self):
        response = self.client.get("/?blank=1")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertRegex(html, r'name="budget"[^>]*value=""')
        self.assertEqual(html.count('<option value="" selected>'), 3)
        self.assertNotIn('id="results"', html)
        self.assertIn("Load sample", html)

    def test_empty_pantry_can_still_get_a_plan(self):
        response = self.client.post("/", data={"budget": "60.00"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="shopping-total"', response.data)

    def test_one_ingredient_works_with_two_unused_rows(self):
        response = self.client.post("/", data={"budget": "60.00", "ingredient_2": "oil", "amount_2": "35"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="shopping-total"', response.data)
        self.assertIn(b"Used from your pantry", response.data)

    def test_amount_on_its_own_prompts_for_an_ingredient(self):
        response = self.client.post("/", data={"budget": "60.00", "amount_1": "200"})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Choose an ingredient for pantry row 1.", response.data)

    def test_duplicate_entries_are_added_together(self):
        self.form.update(amount_1="100", ingredient_4="rice", amount_4="100")
        response = self.client.post("/", data=self.form)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NIS 22.50", response.data)

    def test_photo_suggestions_fill_extra_rows_before_planning(self):
        with patch("app.suggest_ingredients", return_value=["tomato", "onion", "rice"]):
            response = self.client.post("/photo", data=dict(self.form, photo=self.photo_file()))

        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Suggested Tomatoes, Onions.", html)
        self.assertIn('<option value="tomato" selected>', html.split('name="ingredient_4"', 1)[1])
        self.assertIn('<option value="onion" selected>', html.split('name="ingredient_5"', 1)[1])
        self.assertRegex(html, r'name="amount_4"[^>]*value=""')
        self.assertRegex(html, r'name="amount_1"[^>]*value="200"')
        self.assertNotIn('id="results"', html)

        data = dict(self.form, ingredient_4="tomato", amount_4="3", ingredient_5="onion", amount_5="2")
        result = self.client.post("/", data=data)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"NIS 11.50", result.data)

    def test_photo_uses_blank_rows_first(self):
        with patch("app.suggest_ingredients", return_value=["tomato", "onion"]):
            response = self.client.post("/photo", data={"photo": self.photo_file()})

        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('name="ingredient_4"', html)
        first_row = html.split('name="ingredient_1"', 1)[1].split("</select>", 1)[0]
        self.assertIn('<option value="tomato" selected>', first_row)

    def test_invalid_photo_preserves_budget_and_rows(self):
        photo = (BytesIO(b"plain text"), "pantry.jpg")
        response = self.client.post("/photo", data=dict(self.form, photo=photo))

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"image could not be opened", response.data)
        self.assertIn(b'value="30.00"', response.data)
        self.assertIn(b'<option value="rice" selected>', response.data)

    def test_unconfigured_photo_service_explains_how_to_continue(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            response = self.client.post("/photo", data=dict(self.form, photo=self.photo_file()))

        self.assertEqual(response.status_code, 503)
        self.assertIn(b"GEMINI_API_KEY", response.data)
        self.assertIn(b'value="30.00"', response.data)

    def test_photo_size_limit_returns_the_planner_form(self):
        with patch.dict(app.config, {"MAX_CONTENT_LENGTH": 128}):
            response = self.client.post("/photo", data={"photo": self.photo_file()})

        self.assertEqual(response.status_code, 413)
        self.assertIn(b"Choose an image up to 10 MB.", response.data)
        self.assertIn(b"Load sample", response.data)

    @staticmethod
    def photo_file():
        buffer = BytesIO()
        Image.new("RGB", (16, 16), "red").save(buffer, format="PNG")
        buffer.seek(0)
        return buffer, "pantry.png"
