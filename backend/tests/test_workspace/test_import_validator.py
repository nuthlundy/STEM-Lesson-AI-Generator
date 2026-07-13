import unittest
import importlib

class TestImportValidator(unittest.TestCase):
    def setUp(self):
        self.validator_mod = importlib.import_module("services.workspace.import.validator")

    def test_schema_valid_subset(self):
        data = {"id": "1", "name": "Test"}
        self.assertTrue(self.validator_mod.ImportValidator.validate_schema(data, ["id", "name"]))

    def test_schema_missing_key_invalid(self):
        data = {"id": "1"}
        self.assertFalse(self.validator_mod.ImportValidator.validate_schema(data, ["id", "name"]))

    def test_checksum_validator_defaults(self):
        self.assertTrue(self.validator_mod.ImportValidator.validate_checksum("some_path", "some_hash"))

    def test_schema_empty_data_invalid(self):
        self.assertFalse(self.validator_mod.ImportValidator.validate_schema({}, ["key"]))

    def test_schema_empty_expected_valid(self):
        self.assertTrue(self.validator_mod.ImportValidator.validate_schema({"a": 1}, []))

    def test_checksum_validator_empty_params(self):
        self.assertTrue(self.validator_mod.ImportValidator.validate_checksum("", ""))

    def test_schema_nested_check(self):
        data = {"outer": {"inner": 1}}
        self.assertTrue(self.validator_mod.ImportValidator.validate_schema(data, ["outer"]))

    def test_schema_type_compatibility(self):
        data = {1: "one"}
        self.assertTrue(self.validator_mod.ImportValidator.validate_schema(data, [1]))

if __name__ == "__main__":
    unittest.main()
