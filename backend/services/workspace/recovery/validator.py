from typing import Dict, Any

class RecoveryValidator:
    @staticmethod
    def validate_workspace_integrity(workspace_data: Dict[str, Any]) -> bool:
        return "workspace_id" in workspace_data and "root_path" in workspace_data

    @staticmethod
    def validate_project_integrity(project_data: Dict[str, Any]) -> bool:
        return "project_id" in project_data and "project_name" in project_data

    @staticmethod
    def validate_artifact_integrity(artifact_data: Dict[str, Any]) -> bool:
        return True
