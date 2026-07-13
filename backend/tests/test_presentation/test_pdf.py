import unittest
import tempfile
import os
from services.presentation.export.pdf import PdfPresentationExporter

class TestPdfExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = PdfPresentationExporter()

    def test_pdf_export_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "lesson.pdf")
            self.exporter.export("session.json", out_file)
            self.assertTrue(os.path.exists(out_file))

    def test_pdf_validation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "lesson.pdf")
            self.exporter.export("session.json", out_file)
            self.assertTrue(self.exporter.validate(out_file))

    def test_pdf_metadata(self):
        meta = self.exporter.metadata("lesson.pdf")
        self.assertEqual(meta["export_type"], "pdf")

if __name__ == "__main__":
    unittest.main()
