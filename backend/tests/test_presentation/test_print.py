import unittest
import tempfile
import os
from services.presentation.export.print import PrintPresentationExporter

class TestPrintExporter(unittest.TestCase):
    def setUp(self):
        self.exporter = PrintPresentationExporter()

    def test_print_export_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "print_layout.txt")
            self.exporter.export("session.json", out_file)
            self.assertTrue(os.path.exists(out_file))

    def test_print_validation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = os.path.join(tmp_dir, "print_layout.txt")
            self.exporter.export("session.json", out_file)
            self.assertTrue(self.exporter.validate(out_file))

    def test_print_metadata(self):
        meta = self.exporter.metadata("print_layout.txt")
        self.assertEqual(meta["export_type"], "print")

if __name__ == "__main__":
    unittest.main()
