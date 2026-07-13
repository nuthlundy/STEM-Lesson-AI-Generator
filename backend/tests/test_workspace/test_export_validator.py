import unittest
from services.workspace.export.validator import ExportValidator

class TestExportValidator(unittest.TestCase):
    def test_completeness_valid(self):
        data = {"id": "1", "name": "test"}
        self.assertTrue(ExportValidator.validate_completeness(data, ["id", "name"]))

    def test_completeness_missing_invalid(self):
        data = {"id": "1"}
        self.assertFalse(ExportValidator.validate_completeness(data, ["id", "name"]))

    def test_metadata_with_version_valid(self):
        self.assertTrue(ExportValidator.validate_metadata({"version": "1.0"}))

    def test_metadata_with_workspace_id_valid(self):
        self.assertTrue(ExportValidator.validate_metadata({"workspace_id": "ws1"}))

    def test_metadata_with_project_id_valid(self):
        self.assertTrue(ExportValidator.validate_metadata({"project_id": "p1"}))

    def test_metadata_missing_all_invalid(self):
        self.assertFalse(ExportValidator.validate_metadata({"other": "field"}))

    def test_completeness_empty_data_invalid(self):
        self.assertFalse(ExportValidator.validate_completeness({}, ["key"]))

    def test_completeness_empty_required_valid(self):
        self.assertTrue(ExportValidator.validate_completeness({"key": "val"}, []))

if __name__ == "__main__":
    unittest.main()
