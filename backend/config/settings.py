import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "STEM Lesson AI Studio"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # Upload limits
    max_upload_size_mb: int = 50
    upload_dir: str = "uploads/incoming"
    
    class Config:
        env_file = ".env"

settings = Settings()
