import unittest
import tempfile
import os
import json
from services.presentation.utilities.statistics import AnalyticsManager
from services.presentation.engine import PresentationEngine

class TestPresentationAnalytics(unittest.TestCase):
    def test_analytics_manager_report(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = AnalyticsManager()
            mgr.interaction_counts = 5
            mgr.activity_counts = 2
            mgr.elapsed_time = 120.5
            mgr.poll_stats = {"p1": {"0": 3, "1": 1}}
            
            report = mgr.generate_report(tmp_dir)
            self.assertEqual(report["interaction_counts"], 5)
            self.assertEqual(report["poll_statistics"]["p1"]["0"], 3)
            
            out_file = os.path.join(tmp_dir, "presentation_analytics.json")
            self.assertTrue(os.path.exists(out_file))

    def test_engine_analytics_generation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_pptx = os.path.join(tmp_dir, "lesson.pptx")
            with open(dummy_pptx, "w") as f:
                f.write("dummy")
                
            engine = PresentationEngine(workspace_root=tmp_dir)
            engine.initialize()
            engine.process(dummy_pptx)
            
            analytics_path = os.path.join(tmp_dir, "presentation_analytics.json")
            self.assertTrue(os.path.exists(analytics_path))

if __name__ == "__main__":
    unittest.main()
