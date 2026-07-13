from pydantic import BaseModel
from typing import Dict, Any

class UserProfile(BaseModel):
    profile_id: str
    profile_name: str
    preferred_ai_provider: str = "gemini"
    preferred_renderer: str = "html"
    export_defaults: Dict[str, Any] = {}
    language: str = "en"
    theme: str = "light"
    created_timestamp: float
