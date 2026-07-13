import unittest
import tempfile
import os
import json
from services.presentation.export.manager import PresentationExportManager
from services.presentation.export.factory import PresentationExportFactory
from services.presentation.export.base_exporter import BasePresentationExporter
from services.presentation.engine import PresentationEngine

class TestPresentationExportManager(unittest.TestCase):
    def setUp(self):
        self.factory = PresentationExportFactory()
        self.factory.register("pdf", BasePresentationExporter)
        self.manager = PresentationExportManager(factory=self.factory)

    def test_execute_export_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            session_path = os.path.join(tmp_dir, "session.json")
            with open(session_path, "w") as f:
                f.write("{}")
            output_path = os.path.join(tmp_dir, "lesson.pdf")
            
            entry = self.manager.execute_export("pdf", session_path, output_path, workspace_root=tmp_dir)
            self.assertEqual(entry["export_status"], "success")
            self.assertEqual(entry["output_filename"], "lesson.pdf")
            
            report_path = os.path.join(tmp_dir, "presentation_exports.json")
            self.assertTrue(os.path.exists(report_path))

    def test_execute_export_missing_exporter(self):
        with self.assertRaises(ValueError):
            self.manager.execute_export("unsupported", "session.json", "output.txt")

    def test_manager_registration_integration(self):
        mgr = PresentationExportManager()
        self.assertIsNotNone(mgr.factory)

    def test_execute_export_failed_on_exception(self):
        class BrokenExporter(BasePresentationExporter):
            def export(self, s, o):
                raise RuntimeError("Failed")
        self.factory.register("broken", BrokenExporter)
        with tempfile.TemporaryDirectory() as tmp_dir:
            entry = self.manager.execute_export("broken", "session.json", "output.txt", workspace_root=tmp_dir)
            self.assertEqual(entry["export_status"], "failed")

    def test_execute_export_invalid_on_validation_failure(self):
        class InvalidExporter(BasePresentationExporter):
            def validate(self, o):
                return False
        self.factory.register("invalid", InvalidExporter)
        with tempfile.TemporaryDirectory() as tmp_dir:
            entry = self.manager.execute_export("invalid", "session.json", "output.txt", workspace_root=tmp_dir)
            self.assertEqual(entry["export_status"], "invalid")

    def test_exports_history_tracking(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.manager.execute_export("pdf", "s", "o.pdf", workspace_root=tmp_dir)
            self.assertEqual(len(self.manager.exports_history), 1)

    def test_engine_export_manager_registration(self):
        engine = PresentationEngine()
        self.assertIsNone(engine.export_manager)
        engine.initialize()
        self.assertIsNotNone(engine.export_manager)
        self.assertIsNotNone(engine.export_factory)
        engine.shutdown()
        self.assertIsNone(engine.export_manager)

    def test_metadata_report_format(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.manager.execute_export("pdf", "s", "o.pdf", workspace_root=tmp_dir)
            report_path = os.path.join(tmp_dir, "presentation_exports.json")
            with open(report_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("exports", data)
            self.assertEqual(len(data["exports"]), 1)

if __name__ == "__main__":
    unittest.main()
