from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class Settings(BaseModel):
    """Global configuration settings for the entire platform."""
    environment: str = "development"
    workspace: str = "."
    logging: str = "INFO"
    cache: bool = True
    retry_policy: int = 3
    timeout: float = 30.0
    feature_flags: Dict[str, bool] = Field(default_factory=dict)

    model_config = {
        "protected_namespaces": ()
    }
