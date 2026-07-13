import unittest
import tempfile
import os
import json
from services.presentation.engine import PresentationEngine

class TestPresentationDiagnostics(unittest.TestCase):
    def test_diagnostics_file_generation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_pptx = os.path.join(tmp_dir, "lesson.pptx")
            with open(dummy_pptx, "w") as f:
                f.write("dummy")
                
            engine = PresentationEngine(workspace_root=tmp_dir)
            engine.initialize()
            engine.process(dummy_pptx)
            
            diag_file = os.path.join(tmp_dir, "presentation_diagnostics.json")
            self.assertTrue(os.path.exists(diag_file))
            with open(diag_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.assertIn("execution_time", data)
            self.assertIn("module_status", data)
            self.assertIn("validation_statistics", data)
            self.assertIn("optimization_statistics", data)
            self.assertIn("export_statistics", data)
            self.assertIn("memory_usage", data)

    def test_engine_workflow_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_pptx = os.path.join(tmp_dir, "lesson.pptx")
            with open(dummy_pptx, "w") as f:
                f.write("dummy")
                
            engine = PresentationEngine(workspace_root=tmp_dir)
            engine.initialize()
            engine.process(dummy_pptx)
            
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "presentation_summary.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "presentation_validation.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "presentation_quality.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "presentation_exports.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "presentation_delivery.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "lesson.pdf")))

    def test_diagnostics_empty_exports(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            engine = PresentationEngine(workspace_root=tmp_dir)
            engine.generate_diagnostics_report(0.01)
            diag_file = os.path.join(tmp_dir, "presentation_diagnostics.json")
            self.assertTrue(os.path.exists(diag_file))

if __name__ == "__main__":
    unittest.main()
