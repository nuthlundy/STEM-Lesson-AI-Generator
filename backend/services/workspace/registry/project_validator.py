import os
from typing import Dict, Any, List
from services.workspace.registry.project_metadata import ProjectMetadata

class ProjectValidator:
    @staticmethod
    def validate(meta: ProjectMetadata, existing_registry: List[ProjectMetadata]) -> bool:
        if not os.path.exists(meta.workspace_path):
            return False
        if any(p.project_id == meta.project_id for p in existing_registry):
            return False
        if any(p.project_name == meta.project_name for p in existing_registry):
            return False
        return True
