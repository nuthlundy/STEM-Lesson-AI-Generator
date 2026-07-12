from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class Event(BaseModel):
    """Pydantic model representing a canonical pipeline event."""
    event_id: str
    event_name: str
    source_engine: str
    execution_id: Optional[str] = None
    workflow_id: Optional[str] = None
    timestamp: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "protected_namespaces": ()
    }
