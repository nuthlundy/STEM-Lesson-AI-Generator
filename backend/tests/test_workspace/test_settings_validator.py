import unittest
from services.workspace.settings.settings import GlobalSettings
from services.workspace.settings.validator import SettingsValidator

class TestSettingsValidator(unittest.TestCase):
    def setUp(self):
        self.settings = GlobalSettings()

    def test_default_settings_valid(self):
        self.assertTrue(SettingsValidator.validate(self.settings))

    def test_provider_gemini_valid(self):
        self.settings.ai_provider = "gemini"
        self.assertTrue(SettingsValidator.validate(self.settings))

    def test_provider_openai_valid(self):
        self.settings.ai_provider = "openai"
        self.assertTrue(SettingsValidator.validate(self.settings))

    def test_provider_mock_valid(self):
        self.settings.ai_provider = "mock"
        self.assertTrue(SettingsValidator.validate(self.settings))

    def test_provider_unsupported_invalid(self):
        self.settings.ai_provider = "unknown"
        self.assertFalse(SettingsValidator.validate(self.settings))

    def test_renderer_unsupported_invalid(self):
        self.settings.default_renderer = "unknown"
        self.assertFalse(SettingsValidator.validate(self.settings))

    def test_interval_lower_bound_invalid(self):
        self.settings.autosave_interval = 0
        self.assertFalse(SettingsValidator.validate(self.settings))

    def test_interval_upper_bound_invalid(self):
        self.settings.autosave_interval = 90000
        self.assertFalse(SettingsValidator.validate(self.settings))

if __name__ == "__main__":
    unittest.main()
