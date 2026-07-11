import os
from pydantic_settings import BaseSettings

class LanguageIntelligenceConfig(BaseSettings):
    # API configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model_version: str = "gemini-1.5-flash"
    
    # NLP configuration
    default_language: str = "en"
    active_provider: str = os.getenv("LIE_ACTIVE_PROVIDER", "gemini") # 'gemini', 'openai', 'claude', 'deterministic'
    
    class Config:
        env_file = ".env"

lie_config = LanguageIntelligenceConfig()
