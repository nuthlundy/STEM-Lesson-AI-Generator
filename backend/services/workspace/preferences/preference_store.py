import os
import json
from services.workspace.preferences.preferences import UserPreferences

class PreferenceStore:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.preferences_file = os.path.join(storage_path, "preferences.json")

    def load_preferences(self) -> UserPreferences:
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return UserPreferences(**data)
            except Exception:
                pass
        return UserPreferences()

    def save_preferences(self, preferences: UserPreferences) -> None:
        data = preferences.model_dump()
        with open(self.preferences_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
