from typing import Dict, Any
from services.workspace.settings.settings import GlobalSettings

class SettingsValidator:
    SUPPORTED_PROVIDERS = ["gemini", "mock", "openai"]
    SUPPORTED_RENDERERS = ["html", "pdf", "canvas"]

    @staticmethod
    def validate(settings: GlobalSettings) -> bool:
        if settings.ai_provider not in SettingsValidator.SUPPORTED_PROVIDERS:
            return False
        if settings.default_renderer not in SettingsValidator.SUPPORTED_RENDERERS:
            return False
        if settings.autosave_interval <= 0 or settings.autosave_interval > 86400:
            return False
        return True
