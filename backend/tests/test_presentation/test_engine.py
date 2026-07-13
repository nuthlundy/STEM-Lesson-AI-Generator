import unittest
import tempfile
import os
import json
from services.presentation.engine import PresentationEngine
from services.presentation.config import PresentationConfig
from services.presentation.types import PresentationNotFoundError

class TestPresentationEngine(unittest.TestCase):
    def test_missing_file_raises_error(self):
        engine = PresentationEngine()
        with self.assertRaises(PresentationNotFoundError):
            engine.present("non_existent_presentation.pptx")

# Dynamically add 45 test cases with various duration, mode, and presenter view combinations
for i in range(45):
    def make_test_engine(duration, view_mode, enable_presenter):
        def test_func(self):
            with tempfile.TemporaryDirectory() as tmp_dir:
                dummy_pptx = os.path.join(tmp_dir, "lesson.pptx")
                with open(dummy_pptx, "w") as f:
                    f.write("dummy content")
                
                engine = PresentationEngine(workspace_root=tmp_dir)
                config = PresentationConfig(
                    duration_seconds=duration,
                    view_mode=view_mode,
                    enable_presenter_view=enable_presenter
                )
                session = engine.present(dummy_pptx, config)
                
                self.assertEqual(session.duration_seconds, duration)
                self.assertEqual(session.metadata["view_mode"], view_mode)
                self.assertEqual(session.metadata["enable_presenter_view"], enable_presenter)
                
                out_path = os.path.join(tmp_dir, "presentation_session.json")
                self.assertTrue(os.path.exists(out_path))
        return test_func
    setattr(
        TestPresentationEngine,
        f"test_engine_run_{i}",
        make_test_engine(
            duration=300 + i * 10,
            view_mode="standard" if i % 2 == 0 else "expanded",
            enable_presenter=True if i % 3 == 0 else False
        )
    )

if __name__ == "__main__":
    unittest.main()
