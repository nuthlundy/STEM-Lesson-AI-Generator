from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class Provider(BaseModel):
    """Pydantic model representing an external AI provider configuration."""
    provider_name: str
    provider_type: str # e.g. Gemini, OpenAI, Claude, Local LLM
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 4096
    extra_config: Dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "protected_namespaces": ()
    }
