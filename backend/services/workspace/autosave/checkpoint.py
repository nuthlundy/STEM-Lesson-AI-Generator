from pydantic import BaseModel
from typing import List

class AutosaveCheckpoint(BaseModel):
    checkpoint_id: str
    timestamp: float
    project_id: str
    changed_artifacts: List[str] = []
    checksum: str
