import unittest
import tempfile
import os
from services.workspace.recovery.repair import RecoveryRepair
from services.workspace.recovery.validator import RecoveryValidator

class TestRepair(unittest.TestCase):
    def test_repair_missing_metadata(self):
        data = {"id": "p-1"}
        defaults = {"name": "repaired_name"}
        res = RecoveryRepair.repair_missing_metadata(data, defaults)
        self.assertEqual(res["name"], "repaired_name")

    def test_existing_metadata_untouched(self):
        data = {"id": "p-1", "name": "original"}
        defaults = {"name": "repaired_name"}
        res = RecoveryRepair.repair_missing_metadata(data, defaults)
        self.assertEqual(res["name"], "original")

    def test_repair_missing_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            expected = ["sub/file1.json", "file2.json"]
            repaired = RecoveryRepair.repair_missing_artifacts(tmp_dir, expected)
            self.assertEqual(len(repaired), 2)
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "sub/file1.json")))

    def test_repair_missing_artifacts_some_exist(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, "file1.json")
            with open(file_path, "w") as f:
                f.write("existing")
            
            repaired = RecoveryRepair.repair_missing_artifacts(tmp_dir, ["file1.json", "file2.json"])
            self.assertEqual(len(repaired), 1)
            self.assertEqual(repaired[0], "file2.json")

    def test_validator_workspace_valid(self):
        self.assertTrue(RecoveryValidator.validate_workspace_integrity({"workspace_id": "1", "root_path": "."}))

    def test_validator_workspace_invalid(self):
        self.assertFalse(RecoveryValidator.validate_workspace_integrity({"workspace_id": "1"}))

    def test_validator_project_valid(self):
        self.assertTrue(RecoveryValidator.validate_project_integrity({"project_id": "1", "project_name": "Math"}))

    def test_validator_project_invalid(self):
        self.assertFalse(RecoveryValidator.validate_project_integrity({"project_id": "1"}))

if __name__ == "__main__":
    unittest.main()
