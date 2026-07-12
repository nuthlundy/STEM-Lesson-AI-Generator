import os
from pydantic_settings import BaseSettings

class LessonPlanningConfig(BaseSettings):
    # API Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model_version: str = "gemini-1.5-flash"
    
    # Planner Configuration
    active_planner_provider: str = os.getenv("LPE_ACTIVE_PROVIDER", "gemini") # 'gemini', 'deterministic'
    
    class Config:
        env_file = ".env"
        extra = "ignore"

lpe_config = LessonPlanningConfig()
