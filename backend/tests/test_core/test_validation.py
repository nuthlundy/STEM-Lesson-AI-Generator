import unittest
import os
import json
import tempfile
from core.validation import (
    SystemValidator,
    SystemChecks,
    ValidationReporter,
    ValidationError,
    PipelineValidator
)
from core.workflow.pipeline import Pipeline

class TestValidation(unittest.TestCase):
    def test_workspace_check(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            res = SystemChecks.check_workspace(tmp_dir)
            self.assertEqual(res["status"], "Healthy")
            
        res_bad = SystemChecks.check_workspace("non_existent_folder_xyz_123")
        self.assertEqual(res_bad["status"], "Critical")

    def test_configuration_check(self):
        res = SystemChecks.check_configuration()
        self.assertIn(res["status"], ("Healthy", "Warning"))

    def test_plugin_check(self):
        res = SystemChecks.check_plugins()
        self.assertEqual(res["status"], "Healthy")

    def test_artifact_check(self):
        res = SystemChecks.check_artifacts()
        self.assertEqual(res["status"], "Healthy")

    def test_validation_reporter(self):
        checks = [
            {"name": "c1", "status": "Healthy", "message": "OK"},
            {"name": "c2", "status": "Warning", "message": "Warn"}
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = ValidationReporter.generate_report(checks, tmp_dir)
            self.assertEqual(report["status"], "Warning")
            
            file_path = os.path.join(tmp_dir, "system_validation.json")
            self.assertTrue(os.path.exists(file_path))

    def test_critical_failure_raises_exception(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            # SystemValidator.validate_platform with a non-existent workspace root raises ValidationError
            bad_workspace = os.path.join(tmp_dir, "does_not_exist_subfolder")
            with self.assertRaises(ValidationError):
                SystemValidator.validate_platform(bad_workspace)

    def test_pipeline_validator(self):
        p = Pipeline("Empty Pipeline")
        with self.assertRaises(ValidationError):
            PipelineValidator.validate(p)

if __name__ == "__main__":
    unittest.main()
