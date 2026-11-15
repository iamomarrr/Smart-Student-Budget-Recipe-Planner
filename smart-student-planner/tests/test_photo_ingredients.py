from base64 import b64decode
from io import BytesIO
import json
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from PIL import Image, PngImagePlugin

from ai.photo_ingredients import (
    ENDPOINT,
    PhotoAnalysisError,
    PhotoInputError,
    prepare_photo,
    suggest_ingredients,
)
from planner.catalog import Ingredient


def make_photo(size=(40, 30)):
    image = Image.new("RGB", size, "red")
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Comment", "Test metadata")
    buffer = BytesIO()
    image.save(buffer, format="PNG", pnginfo=metadata)
    return buffer.getvalue()


class PhotoIngredientsTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {
            "tomato": Ingredient("Tomatoes", "piece", 3, 600),
            "onion": Ingredient("Onions", "piece", 3, 500),
        }

    def test_resizes_and_discards_photo_metadata(self):
        prepared = prepare_photo(make_photo((2500, 50)))

        with Image.open(BytesIO(prepared)) as result:
            self.assertEqual(result.format, "JPEG")
            self.assertEqual(result.width, 2048)
            self.assertNotIn("Comment", result.info)
            self.assertFalse(result.getexif())

    def test_rejects_non_image_upload(self):
        with self.assertRaisesRegex(PhotoInputError, "image could not be opened"):
            prepare_photo(b"plain text")

    def test_reports_missing_key_before_calling_gemini(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}), patch("ai.photo_ingredients.urlopen") as urlopen:
            with self.assertRaisesRegex(PhotoAnalysisError, "GEMINI_API_KEY"):
                suggest_ingredients(make_photo(), self.catalog)
        urlopen.assert_not_called()

    def test_sends_photo_and_accepts_only_known_unique_ids(self):
        response = {"candidates": [{"content": {"parts": [
            {"text": "Internal processing", "thought": True},
            {"text": '{"ingredient_ids":["tomato","onion","unknown","tomato"]}'},
        ]}}]}

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-only"}), patch(
            "ai.photo_ingredients.urlopen", return_value=BytesIO(json.dumps(response).encode())
        ) as urlopen:
            suggestions = suggest_ingredients(make_photo(), self.catalog)

        self.assertEqual(suggestions, ["tomato", "onion"])
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, ENDPOINT)
        self.assertEqual(dict(request.header_items())["X-goog-api-key"], "test-only")
        body = json.loads(request.data)
        image = body["contents"][0]["parts"][1]["inlineData"]
        self.assertEqual(image["mimeType"], "image/jpeg")
        with Image.open(BytesIO(b64decode(image["data"]))) as sent:
            self.assertEqual(sent.format, "JPEG")
        schema = body["generationConfig"]["responseJsonSchema"]
        self.assertEqual(schema["properties"]["ingredient_ids"]["items"]["enum"], ["tomato", "onion"])

    def test_handles_missing_analysis_result(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-only"}), patch(
            "ai.photo_ingredients.urlopen", return_value=BytesIO(b'{"candidates":[]}')
        ):
            with self.assertRaisesRegex(PhotoAnalysisError, "no usable suggestions"):
                suggest_ingredients(make_photo(), self.catalog)

    def test_reports_gemini_quota_error(self):
        error = HTTPError(ENDPOINT, 429, "Quota", {}, BytesIO())
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-only"}), patch(
            "ai.photo_ingredients.urlopen", side_effect=error
        ):
            with self.assertRaisesRegex(PhotoAnalysisError, "request limit"):
                suggest_ingredients(make_photo(), self.catalog)
