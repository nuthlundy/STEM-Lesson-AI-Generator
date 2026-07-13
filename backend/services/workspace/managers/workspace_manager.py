import os
import json
import time
import uuid
from typing import Dict, Any, List
from services.workspace.schemas import WorkspaceMetadata
from services.workspace.managers.directory_manager import DirectoryManager

class WorkspaceManager:
    def __init__(self) -> None:
        self.active_workspaces: Dict[str, WorkspaceMetadata] = {}

    def create_workspace(self, root_path: str, directories: List[str]) -> WorkspaceMetadata:
        workspace_id = str(uuid.uuid4())
        DirectoryManager.create_directories(root_path, directories)
        
        meta = WorkspaceMetadata(
            workspace_id=workspace_id,
            root_path=root_path,
            created_at=time.time(),
            status="active",
            directories=directories
        )
        
        config_path = os.path.join(root_path, "workspace.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(meta.model_dump(), f, indent=2)
            
        self.active_workspaces[workspace_id] = meta
        return meta

    def open_workspace(self, root_path: str) -> WorkspaceMetadata:
        config_path = os.path.join(root_path, "workspace.json")
        if not os.path.exists(config_path):
            raise ValueError("Workspace config workspace.json not found")
            
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        meta = WorkspaceMetadata(**data)
        self.active_workspaces[meta.workspace_id] = meta
        return meta

    def close_workspace(self, workspace_id: str) -> None:
        if workspace_id in self.active_workspaces:
            meta = self.active_workspaces[workspace_id]
            meta.status = "closed"
            config_path = os.path.join(meta.root_path, "workspace.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(meta.model_dump(), f, indent=2)
            del self.active_workspaces[workspace_id]

    def validate_workspace(self, root_path: str) -> bool:
        config_path = os.path.join(root_path, "workspace.json")
        if not os.path.exists(config_path):
            return False
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            meta = WorkspaceMetadata(**data)
            return DirectoryManager.verify_structure(root_path, meta.directories)
        except Exception:
            return False
