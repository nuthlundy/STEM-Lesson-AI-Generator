from pydantic import BaseModel

class ProjectMetadata(BaseModel):
    project_id: str
    project_name: str
    creation_date: float
    last_modified: float
    workspace_path: str
    version: str = "1.0.0"
    engine_compatibility: str = ">=1.0.0"
