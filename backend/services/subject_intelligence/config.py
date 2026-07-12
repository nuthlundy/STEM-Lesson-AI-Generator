import os
from pydantic_settings import BaseSettings

class SubjectIntelligenceConfig(BaseSettings):
    # API configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model_version: str = "gemini-1.5-flash"
    
    # Subject configuration
    active_subject_provider: str = os.getenv("SIE_ACTIVE_PROVIDER", "gemini") # 'gemini', 'deterministic'
    default_subject: str = "math" # default STEM subject mapping
    
    class Config:
        env_file = ".env"
        extra = "ignore"

sie_config = SubjectIntelligenceConfig()
