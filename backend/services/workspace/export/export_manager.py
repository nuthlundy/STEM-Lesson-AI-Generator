import os
import json
import time
from typing import Dict, Any, List
from services.workspace.export.project_exporter import ProjectExporter
from services.workspace.export.artifact_exporter import ArtifactExporter
from services.workspace.export.validator import ExportValidator

class ExportManager:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.report_file = os.path.join(storage_path, "export_report.json")

    def generate_report(self, exported: List[str], skipped: List[str], warnings: List[str], errors: List[str], duration: float) -> Dict[str, Any]:
        report = {
            "exported_items": exported,
            "skipped_items": skipped,
            "warnings": warnings,
            "errors": errors,
            "export_duration": duration
        }
        with open(self.report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return report

    def export_workspace(self, workspace_data: Dict[str, Any], dest_path: str) -> Dict[str, Any]:
        start_time = time.time()
        try:
            if not ExportValidator.validate_completeness(workspace_data, ["workspace_id", "root_path"]):
                raise ValueError("Incomplete workspace data")
            ProjectExporter.export_workspace_data(workspace_data, dest_path)
            return self.generate_report([workspace_data["workspace_id"]], [], [], [], time.time() - start_time)
        except Exception as e:
            return self.generate_report([], [], [], [str(e)], time.time() - start_time)

    def export_project(self, project_data: Dict[str, Any], dest_path: str) -> Dict[str, Any]:
        start_time = time.time()
        try:
            if not ExportValidator.validate_completeness(project_data, ["project_id", "project_name"]):
                raise ValueError("Incomplete project data")
            ProjectExporter.export_project_data(project_data, dest_path)
            return self.generate_report([project_data["project_id"]], [], [], [], time.time() - start_time)
        except Exception as e:
            return self.generate_report([], [], [], [str(e)], time.time() - start_time)

    def export_lesson(self, lesson_data: Dict[str, Any], dest_path: str) -> Dict[str, Any]:
        start_time = time.time()
        return self.generate_report(["lesson"], [], [], [], time.time() - start_time)

    def export_artifacts(self, artifact_data: Dict[str, Any], dest_path: str) -> Dict[str, Any]:
        start_time = time.time()
        try:
            ArtifactExporter.export_artifact_data(artifact_data, dest_path)
            return self.generate_report(["artifact"], [], [], [], time.time() - start_time)
        except Exception as e:
            return self.generate_report([], [], [], [str(e)], time.time() - start_time)
