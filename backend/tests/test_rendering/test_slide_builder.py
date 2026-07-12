import unittest
import tempfile
import os
import json
from services.rendering.slide_builder import SlideBuilder
from services.rendering.validation import SlideValidator, RenderingValidationError

class TestSlideBuilderAndValidation(unittest.TestCase):
    def setUp(self):
        self.valid_lesson_render = {
            "version": "1.0",
            "slides": [
                {
                    "title": "Welcome Slide",
                    "points": ["Topic introductory details"]
                }
            ],
            "metadata": {"title": "Robotics Intro"}
        }

    def test_slide_builder_presentation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = os.path.join(tmp_dir, "lesson_render.json")
            with open(input_path, "w", encoding="utf-8") as f:
                json.dump(self.valid_lesson_render, f)
                
            builder = SlideBuilder(tmp_dir)
            presentation = builder.build_presentation(input_path, "stem")
            
            self.assertEqual(presentation["theme_name"], "stem")
            self.assertEqual(len(presentation["slides"]), 1)
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "lesson_slides.json")))

    def test_validation_missing_title(self):
        slide = {"points": ["No title here"]}
        with self.assertRaises(RenderingValidationError):
            SlideValidator.validate_slide(slide, 0)

    def test_validation_empty_slide(self):
        slide = {"title": "Title"}
        with self.assertRaises(RenderingValidationError):
            SlideValidator.validate_slide(slide, 0)

    def test_validation_overflow(self):
        slide = {"title": "Title", "points": ["P"] * 11}
        with self.assertRaises(RenderingValidationError):
            SlideValidator.validate_slide(slide, 0)

if __name__ == "__main__":
    unittest.main()
