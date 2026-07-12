import unittest
import os
import json
import tempfile
from services.rendering.engine import RenderingEngine
from services.rendering.schemas import PresentationLayoutModel

class TestRenderingEngine(unittest.TestCase):
    def setUp(self):
        self.lesson_plan_data = {
            "title": "Introduction to Robotics",
            "lesson_sections": [
                {
                    "name": "Warmup",
                    "duration_minutes": 5,
                    "description": "Short video demonstration",
                    "teacher_notes": "Prep video beforehand"
                }
            ]
        }

    def test_rendering_engine_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            engine = RenderingEngine(workspace_root=tmp_dir)
            model = engine.render(self.lesson_plan_data, "deterministic")
            
            self.assertIsInstance(model, PresentationLayoutModel)
            
            output_path = os.path.join(tmp_dir, "lesson_render.json")
            self.assertTrue(os.path.exists(output_path))
            
            with open(output_path, "r", encoding="utf-8") as f:
                saved = json.load(f)
            self.assertEqual(saved["metadata"]["title"], "Introduction to Robotics")

    def test_rendering_engine_execute_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = os.path.join(tmp_dir, "lesson_plan.json")
            with open(input_path, "w", encoding="utf-8") as f:
                json.dump(self.lesson_plan_data, f)
                
            engine = RenderingEngine(workspace_root=tmp_dir)
            model = engine.execute("deterministic")
            self.assertEqual(model.metadata["title"], "Introduction to Robotics")
            
            output_path = os.path.join(tmp_dir, "lesson_render.json")
            self.assertTrue(os.path.exists(output_path))

    def test_rendering_engine_missing_file_raises_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            engine = RenderingEngine(workspace_root=tmp_dir)
            with self.assertRaises(FileNotFoundError):
                engine.execute("deterministic")

    def test_rendering_engine_before_render_override(self):
        class CustomEngine(RenderingEngine):
            def before_render(self, lesson_plan_data):
                lesson_plan_data["title"] = "Overridden Title"
                return lesson_plan_data
                
        with tempfile.TemporaryDirectory() as tmp_dir:
            engine = CustomEngine(workspace_root=tmp_dir)
            model = engine.render(self.lesson_plan_data, "deterministic")
            self.assertEqual(model.metadata["title"], "Overridden Title")

    def test_rendering_engine_after_render_override(self):
        called = []
        class CustomEngine(RenderingEngine):
            def after_render(self, model):
                called.append(True)
                
        with tempfile.TemporaryDirectory() as tmp_dir:
            engine = CustomEngine(workspace_root=tmp_dir)
            model = engine.render(self.lesson_plan_data, "deterministic")
            self.assertEqual(called, [True])
            # Verify file was not written
            output_path = os.path.join(tmp_dir, "lesson_render.json")
            self.assertFalse(os.path.exists(output_path))

if __name__ == "__main__":
    unittest.main()
