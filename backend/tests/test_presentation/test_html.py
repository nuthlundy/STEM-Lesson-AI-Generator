import unittest
import tempfile
import os
from services.presentation.export.html import HtmlPresentationExporter

class TestHtmlExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = HtmlPresentationExporter()

    def test_html_export_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "lesson.html")
            self.exporter.export("session.json", out_file)
            self.assertTrue(os.path.exists(out_file))

    def test_html_validation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "lesson.html")
            self.exporter.export("session.json", out_file)
            self.assertTrue(self.exporter.validate(out_file))

    def test_html_metadata(self):
        meta = self.exporter.metadata("lesson.html")
        self.assertEqual(meta["export_type"], "html")

if __name__ == "__main__":
    unittest.main()
