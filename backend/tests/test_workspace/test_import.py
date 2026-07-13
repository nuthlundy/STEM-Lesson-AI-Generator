import unittest
import tempfile
import os
import json
import importlib
from services.workspace.managers.workspace_manager import WorkspaceManager

class TestImportManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        
        import_mod = importlib.import_module("services.workspace.import.import_manager")
        self.manager = import_mod.ImportManager(storage_path=self.storage_path)

        self.valid_proj_file = os.path.join(self.storage_path, "valid_project.json")
        with open(self.valid_proj_file, "w", encoding="utf-8") as f:
            json.dump({
                "project_id": "p-10",
                "project_name": "Chemistry",
                "workspace_path": self.storage_path
            }, f)

        self.valid_ws_file = os.path.join(self.storage_path, "valid_workspace.json")
        with open(self.valid_ws_file, "w", encoding="utf-8") as f:
            json.dump({
                "workspace_id": "ws-10",
                "root_path": self.storage_path,
                "directories": ["src", "assets"]
            }, f)

        self.valid_art_file = os.path.join(self.storage_path, "valid_artifact.json")
        with open(self.valid_art_file, "w", encoding="utf-8") as f:
            json.dump({
                "artifact_id": "art-1",
                "content": "some text"
            }, f)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_import_workspace_success(self):
        res = self.manager.import_workspace(self.valid_ws_file)
        self.assertEqual(len(res["imported_items"]), 1)
        self.assertEqual(res["imported_items"][0], "ws-10")

    def test_import_workspace_failure(self):
        res = self.manager.import_workspace("nonexistent_ws_file.json")
        self.assertEqual(len(res["errors"]), 1)

    def test_import_project_success(self):
        res = self.manager.import_project(self.valid_proj_file)
        self.assertEqual(len(res["imported_items"]), 1)
        self.assertEqual(res["imported_items"][0], "p-10")

    def test_import_project_failure(self):
        res = self.manager.import_project("nonexistent_project_file.json")
        self.assertEqual(len(res["errors"]), 1)

    def test_import_lesson_success(self):
        res = self.manager.import_lesson("dummy_path")
        self.assertEqual(len(res["imported_items"]), 1)

    def test_import_artifacts_success(self):
        res = self.manager.import_artifacts(self.valid_art_file)
        self.assertEqual(len(res["imported_items"]), 1)

    def test_import_artifacts_failure(self):
        res = self.manager.import_artifacts("nonexistent_art_file")
        self.assertEqual(len(res["errors"]), 1)

    def test_workspace_manager_import_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            
            proj_file = os.path.join(tmp_dir, "proj.json")
            with open(proj_file, "w", encoding="utf-8") as f:
                json.dump({
                    "project_id": "p-int",
                    "project_name": "Integrated Project",
                    "workspace_path": tmp_dir
                }, f)
                
            res = mgr.import_project(proj_file)
            self.assertEqual(res["imported_items"][0], "p-int")

if __name__ == "__main__":
    unittest.main()
