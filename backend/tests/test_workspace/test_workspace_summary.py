import unittest
import tempfile
import os
import json
from services.workspace.engine import WorkspaceEngine

class TestWorkspaceSummary(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.engine = WorkspaceEngine(root_path=self.storage_path)
        self.engine.initialize()
        self.engine.load()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_summary_file_creation(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        self.assertTrue(os.path.exists(summary_path))

    def test_summary_registered_projects(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("registered_projects", data)

    def test_summary_active_profile(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("active_profile", data)

    def test_summary_enabled_modules(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertTrue(len(data.get("enabled_modules", [])) > 0)

    def test_summary_autosave_status(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("autosave_status", data)

    def test_summary_recovery_status(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data.get("recovery_status"), "active")

    def test_summary_search_statistics(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("search_statistics", data)

    def test_summary_template_statistics(self):
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("template_statistics", data)

if __name__ == "__main__":
    unittest.main()
