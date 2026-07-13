import unittest
import tempfile
import os
import json
from services.presentation.processors.deterministic_presenter import DeterministicPresenter
from services.presentation.processors.gemini_presenter import GeminiPresenter
from services.presentation.schemas import PresentationSessionModel

class TestPresenters(unittest.TestCase):
    def setUp(self):
        self.session_data = {
            "session_id": "session-123",
            "presentation_path": "lesson.pptx",
            "duration_seconds": 3600,
            "slides": [
                {
                    "slide_index": 0,
                    "title": "Slide 1",
                    "speaker_notes": "Notes 1",
                    "duration_allocated_seconds": 300
                }
            ],
            "metadata": {}
        }

    def test_deterministic_presenter(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session_path = os.path.join(tmp_dir, "presentation_session.json")
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f)

            presenter = DeterministicPresenter()
            session = presenter.present(session_path)
            self.assertEqual(session.session_id, "session-123")
            self.assertEqual(len(session.slides), 1)

    def test_gemini_presenter_enrichment(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session_path = os.path.join(tmp_dir, "presentation_session.json")
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f)

            presenter = GeminiPresenter()
            session = presenter.present(session_path)
            self.assertEqual(session.session_id, "session-123")
            self.assertTrue(session.metadata["ai_presentation_assistant_active"])

if __name__ == "__main__":
    unittest.main()
