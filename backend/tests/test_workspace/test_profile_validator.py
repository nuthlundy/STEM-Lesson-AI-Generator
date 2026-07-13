import unittest
from services.workspace.profiles.profile import UserProfile
from services.workspace.profiles.profile_validator import ProfileValidator

class TestProfileValidator(unittest.TestCase):
    def setUp(self):
        self.profile = UserProfile(
            profile_id="p1",
            profile_name="Math",
            created_timestamp=123.4
        )

    def test_default_profile_valid(self):
        self.assertTrue(ProfileValidator.validate(self.profile, []))

    def test_empty_profile_name_invalid(self):
        self.profile.profile_name = ""
        self.assertFalse(ProfileValidator.validate(self.profile, []))

    def test_provider_gemini_valid(self):
        self.profile.preferred_ai_provider = "gemini"
        self.assertTrue(ProfileValidator.validate(self.profile, []))

    def test_provider_openai_valid(self):
        self.profile.preferred_ai_provider = "openai"
        self.assertTrue(ProfileValidator.validate(self.profile, []))

    def test_provider_mock_valid(self):
        self.profile.preferred_ai_provider = "mock"
        self.assertTrue(ProfileValidator.validate(self.profile, []))

    def test_provider_unsupported_invalid(self):
        self.profile.preferred_ai_provider = "unsupported"
        self.assertFalse(ProfileValidator.validate(self.profile, []))

    def test_renderer_unsupported_invalid(self):
        self.profile.preferred_renderer = "unsupported"
        self.assertFalse(ProfileValidator.validate(self.profile, []))

    def test_duplicate_name_invalid(self):
        dup = UserProfile(
            profile_id="p2",
            profile_name="Math",
            created_timestamp=567.8
        )
        self.assertFalse(ProfileValidator.validate(self.profile, [dup]))

if __name__ == "__main__":
    unittest.main()
