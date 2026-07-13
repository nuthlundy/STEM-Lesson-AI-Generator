from services.workspace.preferences.preferences import UserPreferences

class PreferenceValidator:
    SUPPORTED_LANGUAGES = ["en", "es", "fr"]
    SUPPORTED_THEMES = ["light", "dark", "system"]
    SUPPORTED_AI_PROVIDERS = ["gemini", "mock", "openai"]
    SUPPORTED_EXPORT_FORMATS = ["pdf", "html", "web", "mobile", "offline", "print", "thumbnails"]

    @staticmethod
    def validate(preferences: UserPreferences) -> bool:
        if preferences.preferred_language not in PreferenceValidator.SUPPORTED_LANGUAGES:
            return False
        if preferences.ui_theme not in PreferenceValidator.SUPPORTED_THEMES:
            return False
        if preferences.ai_model_preference not in PreferenceValidator.SUPPORTED_AI_PROVIDERS:
            return False
        if preferences.default_export_format not in PreferenceValidator.SUPPORTED_EXPORT_FORMATS:
            return False
        return True
