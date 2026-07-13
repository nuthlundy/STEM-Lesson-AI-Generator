import unittest
import tempfile
import os
import time
from services.workspace.snapshots.snapshot_manager import SnapshotManager
from services.workspace.snapshots.snapshot import Snapshot
from services.workspace.managers.workspace_manager import WorkspaceManager

class TestSnapshotManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = SnapshotManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_create_snapshot(self):
        snap = self.manager.create_snapshot("p1", self.storage_path, "First backup")
        self.assertEqual(snap.project_id, "p1")
        self.assertEqual(snap.description, "First backup")
        self.assertEqual(len(self.manager.snapshots), 1)

    def test_restore_snapshot_success(self):
        snap = self.manager.create_snapshot("p1", self.storage_path, "First backup")
        self.assertTrue(self.manager.restore_snapshot(snap.snapshot_id, self.storage_path))

    def test_restore_snapshot_checksum_failure(self):
        snap = self.manager.create_snapshot("p1", self.storage_path, "First backup")
        self.assertFalse(self.manager.restore_snapshot(snap.snapshot_id, "different_path_root"))

    def test_delete_snapshot(self):
        snap = self.manager.create_snapshot("p1", self.storage_path, "First backup")
        self.assertTrue(self.manager.delete_snapshot(snap.snapshot_id))
        self.assertEqual(len(self.manager.snapshots), 0)

    def test_list_snapshots(self):
        self.manager.create_snapshot("p1", self.storage_path, "First backup")
        self.assertEqual(len(self.manager.list_snapshots()), 1)

    def test_workspace_manager_snapshot_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            snap = mgr.create_snapshot("p1", "Integrate Snap")
            self.assertEqual(snap.description, "Integrate Snap")
            self.assertTrue(mgr.restore_snapshot(snap.snapshot_id))
            
            history = mgr.registry.history_manager.retrieve_history()
            actions = [h.action for h in history]
            self.assertIn("snapshot_create", actions)
            self.assertIn("snapshot_restore", actions)

if __name__ == "__main__":
    unittest.main()
