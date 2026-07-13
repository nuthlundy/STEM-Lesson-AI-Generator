import os
import json
from typing import Dict, Any, List
from .validator import ImportValidator

class ProjectImporter:
    @staticmethod
    def import_project_data(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Project config file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not ImportValidator.validate_schema(data, ["project_id", "project_name", "workspace_path"]):
            raise ValueError("Invalid project schema metadata")
        return data

    @staticmethod
    def import_workspace_data(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Workspace config file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not ImportValidator.validate_schema(data, ["workspace_id", "root_path", "directories"]):
            raise ValueError("Invalid workspace schema metadata")
        return data
