import unittest

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
