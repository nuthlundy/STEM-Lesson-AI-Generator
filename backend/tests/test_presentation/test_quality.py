import unittest
import tempfile
import os
import json
from services.presentation.quality.analyzer import QualityAnalyzer
from services.presentation.schemas import PresentationSessionModel

class TestPresentationQuality(unittest.TestCase):
    def setUp(self):
        self.analyzer = QualityAnalyzer()
        self.session_data = {
            "session_id": "session-qual",
            "presentation_path": "lesson.pptx",
            "duration_seconds": 3600,
            "slides": [
                {
                    "slide_index": 0,
                    "title": "Introduction",
                    "speaker_notes": "Note 1",
                    "duration_allocated_seconds": 300
                }
            ],
            "metadata": {}
        }

    def test_quality_analysis_perfect_score(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = PresentationSessionModel(**self.session_data)
            report = self.analyzer.analyze_presentation(session, tmp_dir)
            self.assertEqual(report["quality_score"], 100.0)
            self.assertEqual(len(report["accessibility_issues"]), 0)

    def test_quality_accessibility_warning(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.session_data["slides"][0]["title"] = "In"
            session = PresentationSessionModel(**self.session_data)
            report = self.analyzer.analyze_presentation(session, tmp_dir)
            self.assertEqual(report["quality_score"], 90.0)
            self.assertEqual(len(report["accessibility_issues"]), 1)

    def test_quality_report_written(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = PresentationSessionModel(**self.session_data)
            self.analyzer.analyze_presentation(session, tmp_dir)
            report_file = os.path.join(tmp_dir, "presentation_quality.json")
            self.assertTrue(os.path.exists(report_file))

    def test_quality_scoring_calculation(self):
        from services.presentation.quality.scoring import QualityScoring
        self.assertEqual(QualityScoring.calculate_score(0), 100.0)
        self.assertEqual(QualityScoring.calculate_score(5), 50.0)
        self.assertEqual(QualityScoring.calculate_score(15), 0.0)

    def test_quality_accessibility_empty_title(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.session_data["slides"][0]["title"] = ""
            session = PresentationSessionModel(**self.session_data)
            report = self.analyzer.analyze_presentation(session, tmp_dir)
            self.assertEqual(len(report["accessibility_issues"]), 1)

    def test_quality_analyzer_report_fields(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session = PresentationSessionModel(**self.session_data)
            report = self.analyzer.analyze_presentation(session, tmp_dir)
            self.assertIn("readability", report)
            self.assertIn("slide_density", report)

if __name__ == "__main__":
    unittest.main()
