from pydantic import BaseModel

class Snapshot(BaseModel):
    snapshot_id: str
    project_id: str
    creation_timestamp: float
    version: str = "1.0.0"
    description: str
    workspace_checksum: str
