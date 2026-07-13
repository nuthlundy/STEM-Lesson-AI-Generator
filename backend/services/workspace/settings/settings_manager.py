import os
import json
from typing import Dict, Any
from services.workspace.settings.settings import GlobalSettings
from services.workspace.settings.defaults import DEFAULT_SETTINGS
from services.workspace.settings.validator import SettingsValidator

class SettingsManager:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.settings_file = os.path.join(storage_path, "settings.json")
        self.settings = self.load_settings()

    def load_settings(self) -> GlobalSettings:
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                settings = GlobalSettings(**data)
                if SettingsValidator.validate(settings):
                    return settings
            except Exception:
                pass
        return GlobalSettings(**DEFAULT_SETTINGS)

    def save_settings(self) -> None:
        data = self.settings.model_dump()
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def reset_defaults(self) -> None:
        self.settings = GlobalSettings(**DEFAULT_SETTINGS)
        self.save_settings()

    def update_settings(self, updates: Dict[str, Any]) -> bool:
        temp_settings = GlobalSettings(**{**self.settings.model_dump(), **updates})
        if SettingsValidator.validate(temp_settings):
            self.settings = temp_settings
            self.save_settings()
            return True
        return False
