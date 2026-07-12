import unittest
import os
import json
import tempfile
from services.rendering.engine import RenderingEngine
from services.rendering.optimization.validator import VisualDesignValidator

class TestThemedPipeline(unittest.TestCase):
    def setUp(self):
        self.lesson_render_data = {
            "version": "1.0",
            "slides": [
                {
                    "title": "Welcome Slide",
                    "points": ["Topic introductory details"]
                },
                {
                    "title": "Lesson Details",
                    "points": ["Details bullet 1", "Details bullet 2"]
                },
                {
                    "title": "Closing Remarks",
                    "points": ["Thank you!"]
                }
            ],
            "metadata": {"title": "Robotics Intro"}
        }

    def test_pipeline_execution_generates_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            render_path = os.path.join(tmp_dir, "lesson_render.json")
            with open(render_path, "w", encoding="utf-8") as f:
                json.dump(self.lesson_render_data, f)

            engine = RenderingEngine(workspace_root=tmp_dir)
            presentation = engine.execute_themed_pipeline(theme_name="corporate")

            self.assertEqual(presentation["theme_name"], "corporate")
            self.assertEqual(len(presentation["slides"]), 3)
            self.assertEqual(presentation["slides"][0]["template_name"], "title_slide")
            self.assertEqual(presentation["slides"][1]["template_name"], "content_slide")
            self.assertEqual(presentation["slides"][2]["template_name"], "closing_slide")

            themed_path = os.path.join(tmp_dir, "lesson_themed.json")
            self.assertTrue(os.path.exists(themed_path))
            with open(themed_path, "r", encoding="utf-8") as f:
                themed_data = json.load(f)
            self.assertEqual(themed_data["theme_name"], "corporate")

            quality_path = os.path.join(tmp_dir, "render_quality.json")
            self.assertTrue(os.path.exists(quality_path))

    def test_visual_validator_missing_styles(self):
        invalid_presentation = {
            "slides": [
                {
                    "components": []
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            quality = VisualDesignValidator.validate_visuals(invalid_presentation, workspace_root=tmp_dir)
            self.assertEqual(quality["overall_score"], 0.70)
            self.assertIn("Slide 0 is missing theme styles.", quality["issues"])

    def test_visual_validator_missing_font(self):
        invalid_presentation = {
            "slides": [
                {
                    "theme_styles": {
                        "typography": {}
                    },
                    "components": []
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            quality = VisualDesignValidator.validate_visuals(invalid_presentation, workspace_root=tmp_dir)
            self.assertEqual(quality["overall_score"], 0.70)
            self.assertIn("Slide 0 has missing font families.", quality["issues"])

    def test_visual_validator_overflow_warning(self):
        presentation = {
            "slides": [
                {
                    "theme_styles": {
                        "typography": {"font_family": "Arial"}
                    },
                    "components": [{"type": "text"}] * 13
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            quality = VisualDesignValidator.validate_visuals(presentation, workspace_root=tmp_dir)
            self.assertEqual(quality["overall_score"], 0.70)
            self.assertIn("Slide 0 warning: overlapping elements or element overflow.", quality["issues"])

if __name__ == "__main__":
    unittest.main()
