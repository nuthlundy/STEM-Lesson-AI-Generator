from pydantic import BaseModel
from typing import Dict, Any

class GlobalSettings(BaseModel):
    application_version: str = "1.0.0"
    workspace_root: str = "."
    ai_provider: str = "gemini"
    default_renderer: str = "html"
    export_preferences: Dict[str, Any] = {}
    autosave_interval: int = 300
    logging_level: str = "INFO"
