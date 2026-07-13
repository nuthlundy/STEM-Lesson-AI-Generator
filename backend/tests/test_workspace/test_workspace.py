import unittest
import tempfile
import os
from services.workspace.managers.workspace_manager import WorkspaceManager
from services.workspace.factory import WorkspaceFactory
from services.workspace.engine import WorkspaceEngine

class TestWorkspaceManager(unittest.TestCase):
    def setUp(self):
        self.manager = WorkspaceManager()
        self.dirs = ["src", "assets", "exports"]

    def test_create_workspace(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            meta = self.manager.create_workspace(tmp_dir, self.dirs)
            self.assertEqual(meta.status, "active")
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "workspace.json")))

    def test_open_workspace_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.manager.create_workspace(tmp_dir, self.dirs)
            opened = self.manager.open_workspace(tmp_dir)
            self.assertEqual(opened.status, "active")

    def test_open_workspace_missing_config(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(ValueError):
                self.manager.open_workspace(tmp_dir)

    def test_close_workspace(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            meta = self.manager.create_workspace(tmp_dir, self.dirs)
            self.manager.close_workspace(meta.workspace_id)
            self.assertEqual(len(self.manager.active_workspaces), 0)

    def test_validate_workspace_valid(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.manager.create_workspace(tmp_dir, self.dirs)
            self.assertTrue(self.manager.validate_workspace(tmp_dir))

    def test_validate_workspace_missing_dirs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.manager.create_workspace(tmp_dir, self.dirs)
            os.rmdir(os.path.join(tmp_dir, "src"))
            self.assertFalse(self.manager.validate_workspace(tmp_dir))

    def test_factory_creation(self):
        mgr = WorkspaceFactory.create_workspace_manager()
        self.assertIsNotNone(mgr)

    def test_engine_initialization(self):
        engine = WorkspaceEngine()
        self.assertIsNotNone(engine.manager)

if __name__ == "__main__":
    unittest.main()
