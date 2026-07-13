import unittest
import tempfile
import os
import json
from services.workspace.recovery.recovery_manager import RecoveryManager
from services.workspace.recovery.recovery_plan import RecoveryPlan
from services.workspace.autosave.autosave_manager import AutosaveManager
from services.workspace.managers.workspace_manager import WorkspaceManager

class TestRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = RecoveryManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_detect_interrupted_sessions(self):
        self.assertEqual(self.manager.detect_interrupted_sessions(), [])

    def test_recover_workspace_intact(self):
        ws_data = {"workspace_id": "ws1", "root_path": "/path"}
        res = self.manager.recover_workspace(ws_data)
        self.assertEqual(res["recovery_status"], "success")

    def test_recover_workspace_missing_metadata(self):
        ws_data = {"workspace_id": "ws1"}
        res = self.manager.recover_workspace(ws_data)
        self.assertEqual(res["recovery_status"], "failed")

    def test_recover_project_intact(self):
        proj_data = {"project_id": "p1", "project_name": "Math"}
        res = self.manager.recover_project(proj_data)
        self.assertEqual(res["recovery_status"], "success")

    def test_recover_project_repaired(self):
        proj_data = {"project_id": "p1"}
        res = self.manager.recover_project(proj_data)
        self.assertEqual(res["recovery_status"], "success")
        self.assertIn("project_metadata", res["repaired_items"])

    def test_recover_autosave(self):
        res = self.manager.recover_autosave({})
        self.assertEqual(res["recovery_status"], "success")

    def test_rollback_recovery(self):
        self.assertTrue(self.manager.rollback_failed_recovery("r1"))

    def test_workspace_manager_recovery_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            res = mgr.recover_workspace()
            self.assertEqual(res["recovery_status"], "success")

if __name__ == "__main__":
    unittest.main()
