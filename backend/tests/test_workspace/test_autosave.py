import unittest
import tempfile
import os
import time
from services.workspace.autosave.autosave_manager import AutosaveManager
from services.workspace.autosave.checkpoint import AutosaveCheckpoint
from services.workspace.managers.workspace_manager import WorkspaceManager
from services.workspace.registry.project_metadata import ProjectMetadata

class TestAutosave(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = AutosaveManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_enable_autosave(self):
        self.manager.enable_autosave()
        self.assertTrue(self.manager.enabled)

    def test_disable_autosave(self):
        self.manager.enable_autosave()
        self.manager.disable_autosave()
        self.assertFalse(self.manager.enabled)

    def test_trigger_autosave(self):
        chk = self.manager.trigger_autosave("p-1")
        self.assertIsNotNone(chk)
        self.assertEqual(len(self.manager.checkpoints), 1)

    def test_restore_latest_autosave_success(self):
        self.manager.trigger_autosave("p-1")
        self.assertTrue(self.manager.restore_latest_autosave())

    def test_restore_latest_autosave_empty(self):
        self.assertFalse(self.manager.restore_latest_autosave())

    def test_checkpoint_invalid(self):
        invalid_chk = AutosaveCheckpoint(
            checkpoint_id="",
            timestamp=0.0,
            project_id="",
            checksum=""
        )
        from services.workspace.autosave.validator import AutosaveValidator
        self.assertFalse(AutosaveValidator.validate_checkpoint(invalid_chk))

    def test_workspace_manager_autosave_trigger(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            
            p = ProjectMetadata(
                project_id="p-auto",
                project_name="Math",
                creation_date=time.time(),
                last_modified=time.time(),
                workspace_path=tmp_dir
            )
            mgr.registry.register_project(p)
            self.assertEqual(len(mgr.autosave_manager.checkpoints), 1)

    def test_autosave_generation_triggers(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            mgr.generate_lesson()
            mgr.generate_presentation()
            self.assertEqual(len(mgr.autosave_manager.checkpoints), 2)

if __name__ == "__main__":
    unittest.main()
