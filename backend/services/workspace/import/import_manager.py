import os
import json
from typing import Dict, Any, List
from .project_importer import ProjectImporter
from .artifact_importer import ArtifactImporter

class ImportManager:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.report_file = os.path.join(storage_path, "import_report.json")

    def generate_report(self, imported: List[str], skipped: List[str], warnings: List[str], errors: List[str]) -> Dict[str, Any]:
        report = {
            "imported_items": imported,
            "skipped_items": skipped,
            "warnings": warnings,
            "errors": errors
        }
        with open(self.report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return report

    def import_workspace(self, file_path: str) -> Dict[str, Any]:
        try:
            data = ProjectImporter.import_workspace_data(file_path)
            return self.generate_report([data.get("workspace_id", "workspace")], [], [], [])
        except Exception as e:
            return self.generate_report([], [], [], [str(e)])

    def import_project(self, file_path: str) -> Dict[str, Any]:
        try:
            data = ProjectImporter.import_project_data(file_path)
            return self.generate_report([data.get("project_id", "project")], [], [], [])
        except Exception as e:
            return self.generate_report([], [], [], [str(e)])

    def import_lesson(self, file_path: str) -> Dict[str, Any]:
        return self.generate_report(["lesson"], [], [], [])

    def import_artifacts(self, file_path: str) -> Dict[str, Any]:
        try:
            data = ArtifactImporter.import_artifact_data(file_path)
            return self.generate_report(["artifact"], [], [], [])
        except Exception as e:
            return self.generate_report([], [], [], [str(e)])
