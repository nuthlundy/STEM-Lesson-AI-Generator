import unittest
import tempfile
import os
from services.presentation.engine import PresentationEngine
from services.presentation.factory import PresentationPresenterFactory

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
            
            engine.shutdown()
            self.assertFalse(engine._initialized)
            self.assertIsNone(engine._active_session)

    def test_factory_engine_registration(self):
        engine = PresentationPresenterFactory.create_engine(workspace_root="/tmp")
        self.assertIsInstance(engine, PresentationEngine)
        self.assertEqual(engine.workspace_root, "/tmp")

if __name__ == "__main__":
    unittest.main()
