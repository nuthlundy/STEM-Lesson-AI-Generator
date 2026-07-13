import unittest
import tempfile
import os
import time
from services.workspace.registry.project_registry import ProjectRegistry
from services.workspace.registry.project_metadata import ProjectMetadata
from services.workspace.managers.workspace_manager import WorkspaceManager

class TestProjectRegistry(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.registry = ProjectRegistry(storage_path=self.storage_path)
        
        self.ws_path = os.path.join(self.storage_path, "ws1")
        os.makedirs(self.ws_path, exist_ok=True)
        
        self.meta = ProjectMetadata(
            project_id="p1",
            project_name="Math Lesson",
            creation_date=time.time(),
            last_modified=time.time(),
            workspace_path=self.ws_path
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_register_project_success(self):
        self.assertTrue(self.registry.register_project(self.meta))
        self.assertEqual(len(self.registry.projects), 1)

    def test_register_duplicate_id_failure(self):
        self.registry.register_project(self.meta)
        
        dup = ProjectMetadata(
            project_id="p1",
            project_name="Different Name",
            creation_date=time.time(),
            last_modified=time.time(),
            workspace_path=self.ws_path
        )
        self.assertFalse(self.registry.register_project(dup))

    def test_register_duplicate_name_failure(self):
        self.registry.register_project(self.meta)
        
        dup = ProjectMetadata(
            project_id="different_id",
            project_name="Math Lesson",
            creation_date=time.time(),
            last_modified=time.time(),
            workspace_path=self.ws_path
        )
        self.assertFalse(self.registry.register_project(dup))

    def test_register_missing_workspace_path_failure(self):
        meta = ProjectMetadata(
            project_id="different_id",
            project_name="Math Lesson 2",
            creation_date=time.time(),
            last_modified=time.time(),
            workspace_path=os.path.join(self.storage_path, "nonexistent")
        )
        self.assertFalse(self.registry.register_project(meta))

    def test_unregister_project(self):
        self.registry.register_project(self.meta)
        self.assertTrue(self.registry.unregister_project("p1"))
        self.assertEqual(len(self.registry.projects), 0)

    def test_update_project(self):
        self.registry.register_project(self.meta)
        self.assertTrue(self.registry.update_project("p1", {"project_name": "New Name"}))
        self.assertEqual(self.registry.lookup_project("p1").project_name, "New Name")

    def test_project_search_index(self):
        self.registry.register_project(self.meta)
        results = self.registry.index.search("Math")
        self.assertEqual(len(results), 1)

    def test_workspace_manager_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            self.assertIsNotNone(mgr.registry)

if __name__ == "__main__":
    unittest.main()
