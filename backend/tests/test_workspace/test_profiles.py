import unittest
import tempfile
import os
from services.workspace.profiles.profile_manager import ProfileManager
from services.workspace.settings.settings_manager import SettingsManager

class TestProfileManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = ProfileManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_create_profile_success(self):
        p = self.manager.create_profile("John Doe")
        self.assertIsNotNone(p)
        self.assertEqual(p.profile_name, "John Doe")
        self.assertEqual(len(self.manager.profiles), 1)

    def test_create_profile_duplicate_name_failure(self):
        self.manager.create_profile("John Doe")
        p = self.manager.create_profile("John Doe")
        self.assertIsNone(p)

    def test_update_profile_success(self):
        p = self.manager.create_profile("John Doe")
        self.assertTrue(self.manager.update_profile(p.profile_id, {"theme": "dark"}))
        self.assertEqual(self.manager.profiles[0].theme, "dark")

    def test_update_profile_validation_failure(self):
        p = self.manager.create_profile("John Doe")
        self.assertFalse(self.manager.update_profile(p.profile_id, {"preferred_ai_provider": "unsupported"}))

    def test_delete_profile(self):
        p = self.manager.create_profile("John Doe")
        self.assertTrue(self.manager.delete_profile(p.profile_id))
        self.assertEqual(len(self.manager.profiles), 0)

    def test_activate_profile(self):
        p = self.manager.create_profile("John Doe")
        self.assertTrue(self.manager.activate_profile(p.profile_id))
        self.assertEqual(self.manager.active_profile_id, p.profile_id)

    def test_list_profiles(self):
        self.manager.create_profile("John Doe")
        self.assertEqual(len(self.manager.list_profiles()), 1)

    def test_settings_manager_switch_profile(self):
        settings_mgr = SettingsManager(storage_path=self.storage_path)
        self.assertTrue(settings_mgr.switch_profile("p-123"))
        self.assertEqual(settings_mgr.settings.active_profile_id, "p-123")

if __name__ == "__main__":
    unittest.main()
