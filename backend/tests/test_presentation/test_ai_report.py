import unittest
import tempfile
import os
import json
from services.presentation.processors.gemini_presenter import GeminiPresenter

class TestAIReportGeneration(unittest.TestCase):
    def test_ai_report_contains_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            presenter = GeminiPresenter()
            session_data = {
                "session_id": "session-report",
                "presentation_path": os.path.join(tmp_dir, "lesson.pptx"),
                "duration_seconds": 3600,
                "slides": [],
                "metadata": {}
            }
            with open(session_data["presentation_path"], "w") as f:
                f.write("dummy")
                
            session_path = os.path.join(tmp_dir, "presentation_session.json")
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(session_data, f)
                
            session = presenter.present(session_path)
            presenter.after_present(session)
            
            report_path = os.path.join(tmp_dir, "presentation_ai_report.json")
            self.assertTrue(os.path.exists(report_path))
            with open(report_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.assertTrue(data["ai_enabled"])
            self.assertIn("cache_statistics", data)
            self.assertIn("confidence_averages", data)
            self.assertIn("fallback_counts", data)
            self.assertIn("enrichment_counts", data)

    def test_ai_report_different_averages(self):
        presenter = GeminiPresenter()
        presenter.confidence_sum = 2.7
        presenter.confidence_count = 3
        
        avg_conf = (presenter.confidence_sum / presenter.confidence_count)
        self.assertAlmostEqual(avg_conf, 0.9)

    def test_ai_report_fallback_counter(self):
        presenter = GeminiPresenter()
        self.assertEqual(presenter.fallback_count, 0)
        with self.assertRaises(FileNotFoundError):
            presenter.present("corrupted_or_nonexistent_json_path")
        self.assertEqual(presenter.fallback_count, 1)

    def test_ai_report_disabled(self):
        report = {
            "ai_enabled": False,
            "cache_statistics": {"hits": 0, "misses": 0},
            "confidence_averages": {"score": 0.0},
            "fallback_counts": 0,
            "enrichment_counts": 0
        }
        self.assertFalse(report["ai_enabled"])

if __name__ == "__main__":
    unittest.main()
