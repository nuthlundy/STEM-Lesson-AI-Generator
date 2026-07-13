import unittest
import tempfile
import os
from services.presentation.export.thumbnails import ThumbnailPresentationExporter

class TestThumbnailsExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = ThumbnailPresentationExporter()

    def test_thumbnails_export_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "slide_0.png")
            self.exporter.export("session.json", out_file)
            self.assertTrue(os.path.exists(out_file))

    def test_thumbnails_validation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "slide_0.png")
            self.exporter.export("session.json", out_file)
            self.assertTrue(self.exporter.validate(out_file))

    def test_thumbnails_metadata(self):
        meta = self.exporter.metadata("slide_0.png")
        self.assertEqual(meta["export_type"], "thumbnails")

if __name__ == "__main__":
    unittest.main()
