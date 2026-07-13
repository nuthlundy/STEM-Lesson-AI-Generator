from typing import Dict, Any
from services.workspace.preferences.preferences import UserPreferences
from services.workspace.preferences.preference_store import PreferenceStore
from services.workspace.preferences.preference_validator import PreferenceValidator

class PreferenceManager:
    def __init__(self, storage_path: str = ".") -> None:
        self.store = PreferenceStore(storage_path=storage_path)
        self.preferences = self.store.load_preferences()

    def load_preferences(self) -> UserPreferences:
        self.preferences = self.store.load_preferences()
        return self.preferences

    def save_preferences(self) -> None:
        self.store.save_preferences(self.preferences)

    def reset_preferences(self) -> None:
        self.preferences = UserPreferences()
        self.save_preferences()

    def apply_preferences(self, updates: Dict[str, Any]) -> bool:
        cand = UserPreferences(**{**self.preferences.model_dump(), **updates})
        if PreferenceValidator.validate(cand):
            self.preferences = cand
            self.save_preferences()
            return True
        return False
