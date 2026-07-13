import unittest
import tempfile
import os
import json
from services.presentation.engine import PresentationEngine
from services.presentation.factory import PresentationPresenterFactory
from services.presentation.session import PresentationSessionBuilder
from services.presentation.navigation.controller import NavigationController
from services.presentation.timing.timer import PresentationTimer

class TestPresentationSession(unittest.TestCase):
    def test_engine_lifecycle_methods(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_pptx = os.path.join(tmp_dir, "lesson.pptx")
            with open(dummy_pptx, "w") as f:
                f.write("dummy content")
                
            engine = PresentationEngine(workspace_root=tmp_dir)
            self.assertFalse(engine._initialized)
            engine.initialize()
            self.assertTrue(engine._initialized)
            
            session = engine.process(dummy_pptx, presenter_type="deterministic")
            self.assertEqual(engine._active_session.session_id, session.session_id)
            
            delivery_path = os.path.join(tmp_dir, "presentation_delivery.json")
            self.assertTrue(os.path.exists(delivery_path))
            with open(delivery_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("navigation_state", data)
            self.assertIn("presenter_tools", data)
            self.assertIn("timing_information", data)

            engine.shutdown()
            self.assertFalse(engine._initialized)
            self.assertIsNone(engine._active_session)

    def test_factory_engine_registration(self):
        engine = PresentationPresenterFactory.create_engine(workspace_root="/tmp")
        self.assertIsInstance(engine, PresentationEngine)
        self.assertEqual(engine.workspace_root, "/tmp")

    def test_session_builder_direct(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            nav = NavigationController(total_slides=4)
            timer = PresentationTimer()
            timer.start()
            
            data = PresentationSessionBuilder.build_delivery_session(
                workspace_root=tmp_dir,
                navigation=nav,
                timer=timer,
                metadata={"test": "val"}
            )
            self.assertEqual(data["navigation_state"]["current_slide"], 0)
            self.assertEqual(len(data["presenter_tools"]["checklist"]), 5)

if __name__ == "__main__":
    unittest.main()
