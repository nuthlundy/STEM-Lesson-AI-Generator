import os
import json
from typing import List
from services.workspace.profiles.profile import UserProfile

class ProfileStore:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.profiles_file = os.path.join(storage_path, "profiles.json")

    def load_profiles(self) -> List[UserProfile]:
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [UserProfile(**p) for p in data.get("profiles", [])]
            except Exception:
                return []
        return []

    def save_profiles(self, profiles: List[UserProfile]) -> None:
        data = {"profiles": [p.model_dump() for p in profiles]}
        with open(self.profiles_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
