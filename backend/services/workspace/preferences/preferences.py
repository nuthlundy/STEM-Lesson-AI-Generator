from pydantic import BaseModel
from typing import Dict, Any

class UserPreferences(BaseModel):
    preferred_language: str = "en"
    ui_theme: str = "light"
    ai_model_preference: str = "gemini"
    default_export_format: str = "html"
    default_lesson_template: str = "standard"
    notification_settings: Dict[str, Any] = {}
    accessibility_options: Dict[str, Any] = {}
