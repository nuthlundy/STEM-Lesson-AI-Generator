import unittest
import tempfile
import os
import json
from services.presentation.documentation.generator import DocumentationGenerator
from services.presentation.schemas import PresentationSessionModel

class TestPresentationDocumentation(unittest.TestCase):
    def setUp(self):
        self.session = PresentationSessionModel(
            session_id="session-doc",
            presentation_path="lesson.pptx",
            duration_seconds=3600,
            slides=[],
            metadata={"theme": "dark"}
        )

    def test_summary_file_generation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            summary = DocumentationGenerator.generate_summary(self.session, tmp_dir)
            self.assertEqual(summary["presentation_metadata"]["theme"], "dark")
            
            out_file = os.path.join(tmp_dir, "presentation_summary.json")
            self.assertTrue(os.path.exists(out_file))

    def test_summary_validation_defaults(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            summary = DocumentationGenerator.generate_summary(self.session, tmp_dir)
            self.assertEqual(summary["validation_summary"]["status"], "passed")

    def test_summary_quality_defaults(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            summary = DocumentationGenerator.generate_summary(self.session, tmp_dir)
            self.assertEqual(summary["quality_summary"]["score"], 100.0)

    def test_summary_ai_active_defaults(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            summary = DocumentationGenerator.generate_summary(self.session, tmp_dir)
            self.assertFalse(summary["AI_summary"]["assistant_active"])

    def test_summary_engine_version(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            summary = DocumentationGenerator.generate_summary(self.session, tmp_dir)
            self.assertEqual(summary["engine_version"], "1.0.0")

if __name__ == "__main__":
    unittest.main()
