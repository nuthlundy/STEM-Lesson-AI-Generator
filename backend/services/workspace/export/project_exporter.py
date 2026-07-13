import os
import json
from typing import Dict, Any

class ProjectExporter:
    @staticmethod
    def export_project_data(project_data: Dict[str, Any], dest_path: str) -> None:
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2)

    @staticmethod
    def export_workspace_data(workspace_data: Dict[str, Any], dest_path: str) -> None:
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(workspace_data, f, indent=2)
