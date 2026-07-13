import unittest
import tempfile
import os
from services.workspace.preferences.preference_manager import PreferenceManager
from services.workspace.preferences.preferences import UserPreferences
from services.workspace.profiles.profile_manager import ProfileManager
from services.workspace.settings.settings_manager import SettingsManager

class TestPreferenceManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = PreferenceManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_default_preferences_load(self):
        prefs = self.manager.preferences
        self.assertEqual(prefs.preferred_language, "en")
        self.assertEqual(prefs.ui_theme, "light")

    def test_save_preferences(self):
        self.manager.preferences.preferred_language = "es"
        self.manager.save_preferences()
        
        new_manager = PreferenceManager(storage_path=self.storage_path)
        self.assertEqual(new_manager.preferences.preferred_language, "es")

    def test_reset_preferences(self):
        self.manager.preferences.preferred_language = "es"
        self.manager.save_preferences()
        self.manager.reset_preferences()
        self.assertEqual(self.manager.preferences.preferred_language, "en")

    def test_apply_preferences_success(self):
        self.assertTrue(self.manager.apply_preferences({"preferred_language": "fr"}))
        self.assertEqual(self.manager.preferences.preferred_language, "fr")

    def test_apply_preferences_validation_failure(self):
        self.assertFalse(self.manager.apply_preferences({"preferred_language": "invalid_lang"}))
        self.assertEqual(self.manager.preferences.preferred_language, "en")

    def test_profile_integration_syncs_preferences(self):
        profile_mgr = ProfileManager(storage_path=self.storage_path)
        p = profile_mgr.create_profile("User1", ai_provider="openai", renderer="pdf", language="es", theme="dark")
        self.assertTrue(profile_mgr.activate_profile(p.profile_id))
        
        self.assertEqual(profile_mgr.preference_manager.preferences.preferred_language, "es")
        self.assertEqual(profile_mgr.preference_manager.preferences.ui_theme, "dark")
        self.assertEqual(profile_mgr.preference_manager.preferences.ai_model_preference, "openai")
        self.assertEqual(profile_mgr.preference_manager.preferences.default_export_format, "pdf")

    def test_settings_manager_override_preference(self):
        settings_mgr = SettingsManager(storage_path=self.storage_path)
        self.assertEqual(settings_mgr.get_effective_setting("ai_provider"), "gemini")
        
        settings_mgr.preference_manager.apply_preferences({"ai_model_preference": "openai"})
        self.assertEqual(settings_mgr.get_effective_setting("ai_provider"), "openai")

    def test_preferences_model_fields(self):
        p = UserPreferences()
        self.assertEqual(p.default_lesson_template, "standard")

if __name__ == "__main__":
    unittest.main()
