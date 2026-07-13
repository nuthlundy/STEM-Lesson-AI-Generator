import unittest
import tempfile
import os
import json
from services.presentation.processors.gemini_presenter import GeminiPresenter
from services.presentation.schemas import PresentationSessionModel, PresentationAIMetadata, SpeakingSuggestion, ConfidenceScore
from services.presentation.utils.merge_engine import PresentationAIMergeEngine

class TestAIPresenterIntegration(unittest.TestCase):
    def setUp(self):
        self.session_data = {
            "session_id": "session-ai",
            "presentation_path": "lesson.pptx",
            "duration_seconds": 3600,
            "slides": [
                {
                    "slide_index": 0,
                    "title": "Intro",
                    "speaker_notes": "Deterministic notes",
                    "duration_allocated_seconds": 300
                }
            ],
            "metadata": {}
        }

    def test_ai_presenter_enrichment(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session_path = os.path.join(tmp_dir, "presentation_session.json")
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f)
                
            presenter = GeminiPresenter()
            presentation_file = os.path.join(tmp_dir, "lesson.pptx")
            with open(presentation_file, "w") as f:
                f.write("dummy")
                
            self.session_data["presentation_path"] = presentation_file
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f)
                
            session = presenter.present(session_path)
            self.assertTrue(session.metadata["ai_presentation_assistant_active"])
            self.assertIsNotNone(session.ai_metadata)
            self.assertEqual(len(session.ai_metadata.speaking_suggestions), 1)
            self.assertEqual(len(session.ai_metadata.audience_questions), 1)
            self.assertEqual(len(session.ai_metadata.discussion_prompts), 1)

    def test_deterministic_primacy(self):
        session = PresentationSessionModel(**self.session_data)
        session.ai_metadata = PresentationAIMetadata(
            speaking_suggestions=[
                SpeakingSuggestion(
                    slide_index=0,
                    suggestion="Deterministic Suggestion",
                    confidence=ConfidenceScore(score=1.0)
                )
            ]
        )
        ai_data = PresentationAIMetadata(
            speaking_suggestions=[
                SpeakingSuggestion(
                    slide_index=0,
                    suggestion="Deterministic Suggestion",
                    confidence=ConfidenceScore(score=0.5)
                ),
                SpeakingSuggestion(
                    slide_index=0,
                    suggestion="AI Suggestion",
                    confidence=ConfidenceScore(score=0.5)
                )
            ]
        )
        
        merged = PresentationAIMergeEngine.merge(session, ai_data)
        self.assertEqual(len(merged.ai_metadata.speaking_suggestions), 2)

    def test_ai_presenter_cache_hits(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            presenter = GeminiPresenter()
            presentation_file = os.path.join(tmp_dir, "lesson.pptx")
            with open(presentation_file, "w") as f:
                f.write("dummy")
                
            self.session_data["presentation_path"] = presentation_file
            session_path = os.path.join(tmp_dir, "presentation_session.json")
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f)
                
            presenter.present(session_path)
            self.assertEqual(presenter.cache_misses, 1)
            
            presenter.present(session_path)
            self.assertEqual(presenter.cache_hits, 1)

    def test_ai_presenter_fallback_on_error(self):
        presenter = GeminiPresenter()
        with self.assertRaises(Exception):
            presenter.present("non_existent_session.json")

    def test_ai_presenter_empty_slides(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            presenter = GeminiPresenter()
            presentation_file = os.path.join(tmp_dir, "lesson.pptx")
            with open(presentation_file, "w") as f:
                f.write("dummy")
                
            empty_session = {
                "session_id": "session-empty",
                "presentation_path": presentation_file,
                "duration_seconds": 3600,
                "slides": [],
                "metadata": {}
            }
            session_path = os.path.join(tmp_dir, "presentation_session.json")
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(empty_session, f)
                
            session = presenter.present(session_path)
            self.assertEqual(len(session.slides), 0)

if __name__ == "__main__":
    unittest.main()
