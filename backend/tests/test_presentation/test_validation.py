import unittest
import tempfile
import os
import json
from services.presentation.validation.validator import PresentationValidator
from services.presentation.schemas import PresentationSessionModel

class TestPresentationValidation(unittest.TestCase):
    def setUp(self):
        self.validator = PresentationValidator()
        self.session_data = {
            "session_id": "session-val",
            "presentation_path": "lesson.pptx",
            "duration_seconds": 3600,
            "slides": [
                {
                    "slide_index": 0,
                    "title": "Slide 1",
                    "speaker_notes": "Note 1",
                    "duration_allocated_seconds": 300
                }
            ],
            "metadata": {
                "objectives": ["Goal 1"]
            }
        }

    def test_validation_pipeline_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = PresentationSessionModel(**self.session_data)
            report = self.validator.validate_session(session, tmp_dir)
            self.assertEqual(report["validation_status"], "passed")
            self.assertEqual(len(report["errors"]), 0)

    def test_validation_slide_sequence_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.session_data["slides"][0]["slide_index"] = 5
            session = PresentationSessionModel(**self.session_data)
            report = self.validator.validate_session(session, tmp_dir)
            self.assertEqual(report["validation_status"], "failed")
            self.assertIn("discontinuous", report["errors"][0])

    def test_validation_missing_notes_warning(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.session_data["slides"][0]["speaker_notes"] = ""
            session = PresentationSessionModel(**self.session_data)
            report = self.validator.validate_session(session, tmp_dir)
            self.assertIn("missing speaker notes", report["warnings"][0])

    def test_validation_missing_objectives(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            del self.session_data["metadata"]["objectives"]
            session = PresentationSessionModel(**self.session_data)
            report = self.validator.validate_session(session, tmp_dir)
            self.assertIn("missing learning objectives", report["warnings"][0])

    def test_validation_report_file_written(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = PresentationSessionModel(**self.session_data)
            self.validator.validate_session(session, tmp_dir)
            report_file = os.path.join(tmp_dir, "presentation_validation.json")
            self.assertTrue(os.path.exists(report_file))

    def test_validation_empty_slides(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.session_data["slides"] = []
            session = PresentationSessionModel(**self.session_data)
            report = self.validator.validate_session(session, tmp_dir)
            self.assertEqual(report["validation_status"], "passed")

if __name__ == "__main__":
    unittest.main()
