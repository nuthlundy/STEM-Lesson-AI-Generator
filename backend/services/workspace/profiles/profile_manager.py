import time
import uuid
from typing import List, Dict, Any, Optional
from services.workspace.profiles.profile import UserProfile
from services.workspace.profiles.profile_store import ProfileStore
from services.workspace.profiles.profile_validator import ProfileValidator

class ProfileManager:
    def __init__(self, storage_path: str = ".") -> None:
        self.store = ProfileStore(storage_path=storage_path)
        self.profiles: List[UserProfile] = self.store.load_profiles()
        self.active_profile_id: Optional[str] = None

    def create_profile(self, name: str, ai_provider: str = "gemini", renderer: str = "html", export_defaults: Dict[str, Any] = None, language: str = "en", theme: str = "light") -> Optional[UserProfile]:
        profile_id = str(uuid.uuid4())
        profile = UserProfile(
            profile_id=profile_id,
            profile_name=name,
            preferred_ai_provider=ai_provider,
            preferred_renderer=renderer,
            export_defaults=export_defaults or {},
            language=language,
            theme=theme,
            created_timestamp=time.time()
        )
        if ProfileValidator.validate(profile, self.profiles):
            self.profiles.append(profile)
            self.store.save_profiles(self.profiles)
            return profile
        return None

    def update_profile(self, profile_id: str, updates: Dict[str, Any]) -> bool:
        for profile in self.profiles:
            if profile.profile_id == profile_id:
                cand = UserProfile(**{**profile.model_dump(), **updates})
                if ProfileValidator.validate(cand, self.profiles):
                    for k, v in updates.items():
                        if hasattr(profile, k):
                            setattr(profile, k, v)
                    self.store.save_profiles(self.profiles)
                    return True
        return False

    def delete_profile(self, profile_id: str) -> bool:
        for i, p in enumerate(self.profiles):
            if p.profile_id == profile_id:
                self.profiles.pop(i)
                if self.active_profile_id == profile_id:
                    self.active_profile_id = None
                self.store.save_profiles(self.profiles)
                return True
        return False

    def activate_profile(self, profile_id: str) -> bool:
        for p in self.profiles:
            if p.profile_id == profile_id:
                self.active_profile_id = profile_id
                return True
        return False

    def list_profiles(self) -> List[UserProfile]:
        return list(self.profiles)
