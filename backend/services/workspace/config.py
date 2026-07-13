from pydantic import BaseModel

class WorkspaceConfig(BaseModel):
    workspace_name: str = "default"
    root_path: str = "."
