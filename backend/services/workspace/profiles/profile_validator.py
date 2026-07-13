from typing import List
from services.workspace.profiles.profile import UserProfile

class ProfileValidator:
    SUPPORTED_PROVIDERS = ["gemini", "mock", "openai"]
    SUPPORTED_RENDERERS = ["html", "pdf", "canvas"]

    @staticmethod
    def validate(profile: UserProfile, existing_profiles: List[UserProfile]) -> bool:
        if not profile.profile_name or not profile.profile_id:
            return False
        if profile.preferred_ai_provider not in ProfileValidator.SUPPORTED_PROVIDERS:
            return False
        if profile.preferred_renderer not in ProfileValidator.SUPPORTED_RENDERERS:
            return False
        for p in existing_profiles:
            if p.profile_id != profile.profile_id and p.profile_name == profile.profile_name:
                return False
        return True
