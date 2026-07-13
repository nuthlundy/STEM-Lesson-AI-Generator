import unittest
import tempfile
import os
from services.workspace.settings.settings_manager import SettingsManager
from services.workspace.settings.settings import GlobalSettings
from services.workspace.managers.workspace_manager import WorkspaceManager

class TestSettingsManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = SettingsManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_default_settings_load(self):
        settings = self.manager.settings
        self.assertEqual(settings.ai_provider, "gemini")
        self.assertEqual(settings.default_renderer, "html")

    def test_save_settings(self):
        self.manager.settings.ai_provider = "openai"
        self.manager.save_settings()
        
        new_manager = SettingsManager(storage_path=self.storage_path)
        self.assertEqual(new_manager.settings.ai_provider, "openai")

    def test_reset_defaults(self):
        self.manager.settings.ai_provider = "openai"
        self.manager.save_settings()
        self.manager.reset_defaults()
        self.assertEqual(self.manager.settings.ai_provider, "gemini")

    def test_update_settings_success(self):
        self.assertTrue(self.manager.update_settings({"ai_provider": "openai"}))
        self.assertEqual(self.manager.settings.ai_provider, "openai")

    def test_update_settings_validation_failure(self):
        self.assertFalse(self.manager.update_settings({"ai_provider": "invalid_provider"}))
        self.assertEqual(self.manager.settings.ai_provider, "gemini")

    def test_load_corrupted_json_falls_back_to_defaults(self):
        with open(self.manager.settings_file, "w") as f:
            f.write("{corrupt")
        self.assertEqual(self.manager.load_settings().ai_provider, "gemini")

    def test_settings_fields_access(self):
        s = GlobalSettings()
        self.assertEqual(s.autosave_interval, 300)

    def test_workspace_manager_settings_integration(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            self.assertIsNotNone(mgr.settings_manager)
            self.assertEqual(mgr.settings_manager.settings.ai_provider, "gemini")

if __name__ == "__main__":
    unittest.main()
