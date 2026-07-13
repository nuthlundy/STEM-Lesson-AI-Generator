import unittest
import tempfile
import os
from services.presentation.export.offline import OfflinePresentationExporter

class TestOfflineExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = OfflinePresentationExporter()

    def test_offline_export_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "lesson_package.zip")
            self.exporter.export("session.json", out_file)
            self.assertTrue(os.path.exists(out_file))

    def test_offline_validation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "lesson_package.zip")
            self.exporter.export("session.json", out_file)
            self.assertTrue(self.exporter.validate(out_file))

    def test_offline_metadata(self):
        meta = self.exporter.metadata("lesson_package.zip")
        self.assertEqual(meta["export_type"], "offline")

if __name__ == "__main__":
    unittest.main()
