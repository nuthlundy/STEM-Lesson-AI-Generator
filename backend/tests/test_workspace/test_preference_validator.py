import unittest
from services.workspace.preferences.preferences import UserPreferences
from services.workspace.preferences.preference_validator import PreferenceValidator

class TestPreferenceValidator(unittest.TestCase):
    def setUp(self):
        self.prefs = UserPreferences()

    def test_default_preferences_valid(self):
        self.assertTrue(PreferenceValidator.validate(self.prefs))

    def test_language_en_valid(self):
        self.prefs.preferred_language = "en"
        self.assertTrue(PreferenceValidator.validate(self.prefs))

    def test_language_es_valid(self):
        self.prefs.preferred_language = "es"
        self.assertTrue(PreferenceValidator.validate(self.prefs))

    def test_language_fr_valid(self):
        self.prefs.preferred_language = "fr"
        self.assertTrue(PreferenceValidator.validate(self.prefs))

    def test_language_unsupported_invalid(self):
        self.prefs.preferred_language = "unsupported"
        self.assertFalse(PreferenceValidator.validate(self.prefs))

    def test_theme_unsupported_invalid(self):
        self.prefs.ui_theme = "unsupported"
        self.assertFalse(PreferenceValidator.validate(self.prefs))

    def test_provider_unsupported_invalid(self):
        self.prefs.ai_model_preference = "unsupported"
        self.assertFalse(PreferenceValidator.validate(self.prefs))

    def test_export_format_unsupported_invalid(self):
        self.prefs.default_export_format = "unsupported"
        self.assertFalse(PreferenceValidator.validate(self.prefs))

if __name__ == "__main__":
    unittest.main()
