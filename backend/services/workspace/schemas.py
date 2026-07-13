from pydantic import BaseModel
from typing import List

class WorkspaceMetadata(BaseModel):
    workspace_id: str
    root_path: str
    created_at: float
    status: str
    directories: List[str]
