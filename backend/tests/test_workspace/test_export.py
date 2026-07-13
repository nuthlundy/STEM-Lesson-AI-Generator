import unittest
import tempfile
import os
import time
from services.workspace.export.export_manager import ExportManager
from services.workspace.managers.workspace_manager import WorkspaceManager
from services.workspace.registry.project_metadata import ProjectMetadata

class TestExportManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = ExportManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_export_workspace_success(self):
        ws_data = {"workspace_id": "ws1", "root_path": "/path"}
        dest = os.path.join(self.storage_path, "ws_export.json")
        res = self.manager.export_workspace(ws_data, dest)
        self.assertEqual(len(res["exported_items"]), 1)
        self.assertTrue(os.path.exists(dest))

    def test_export_workspace_failure(self):
        ws_data = {"workspace_id": "ws1"}
        dest = os.path.join(self.storage_path, "ws_export_fail.json")
        res = self.manager.export_workspace(ws_data, dest)
        self.assertEqual(len(res["errors"]), 1)

    def test_export_project_success(self):
        proj_data = {"project_id": "p1", "project_name": "Math"}
        dest = os.path.join(self.storage_path, "proj_export.json")
        res = self.manager.export_project(proj_data, dest)
        self.assertEqual(len(res["exported_items"]), 1)
        self.assertTrue(os.path.exists(dest))

    def test_export_project_failure(self):
        proj_data = {"project_id": "p1"}
        dest = os.path.join(self.storage_path, "proj_export_fail.json")
        res = self.manager.export_project(proj_data, dest)
        self.assertEqual(len(res["errors"]), 1)

    def test_export_lesson(self):
        res = self.manager.export_lesson({}, "dummy")
        self.assertEqual(len(res["exported_items"]), 1)

    def test_export_artifacts_success(self):
        art_data = {"id": "art-1"}
        dest = os.path.join(self.storage_path, "art_export.json")
        res = self.manager.export_artifacts(art_data, dest)
        self.assertEqual(len(res["exported_items"]), 1)
        self.assertTrue(os.path.exists(dest))

    def test_workspace_manager_export_project_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            ws_path = os.path.join(tmp_dir, "ws1")
            os.makedirs(ws_path, exist_ok=True)
            
            p = ProjectMetadata(
                project_id="p-1",
                project_name="Math",
                creation_date=time.time(),
                last_modified=time.time(),
                workspace_path=ws_path
            )
            mgr.registry.register_project(p)
            
            dest = os.path.join(tmp_dir, "exported_proj.json")
            res = mgr.export_project("p-1", dest)
            self.assertEqual(res["exported_items"][0], "p-1")
            self.assertTrue(os.path.exists(dest))

    def test_workspace_manager_export_workspace_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            meta = mgr.create_workspace(tmp_dir, ["src"])
            
            dest = os.path.join(tmp_dir, "exported_ws.json")
            res = mgr.export_workspace(meta.workspace_id, dest)
            self.assertEqual(res["exported_items"][0], meta.workspace_id)
            self.assertTrue(os.path.exists(dest))

if __name__ == "__main__":
    unittest.main()
