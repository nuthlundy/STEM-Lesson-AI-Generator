import unittest
import tempfile
import os
from services.presentation.export.mobile import MobilePresentationExporter

class TestMobileExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = MobilePresentationExporter()

    def test_mobile_export_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "mobile_package.json")
            self.exporter.export("session.json", out_file)
            self.assertTrue(os.path.exists(out_file))

    def test_mobile_validation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "mobile_package.json")
            self.exporter.export("session.json", out_file)
            self.assertTrue(self.exporter.validate(out_file))

    def test_mobile_metadata(self):
        meta = self.exporter.metadata("mobile_package.json")
        self.assertEqual(meta["export_type"], "mobile")

if __name__ == "__main__":
    unittest.main()
