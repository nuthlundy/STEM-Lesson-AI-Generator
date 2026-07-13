from pydantic import BaseModel
from typing import Dict, Any, Optional

class HistoryEntry(BaseModel):
    timestamp: float
    action: str
    engine: str
    artifact: Optional[str] = None
    project_id: str
    user_metadata: Dict[str, Any] = {}
