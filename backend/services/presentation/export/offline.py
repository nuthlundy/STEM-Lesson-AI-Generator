from services.presentation.export.base_exporter import BasePresentationExporter
import os
import zipfile
from typing import Dict, Any

class OfflinePresentationExporter(BasePresentationExporter):
    def export(self, session_path: str, output_path: str) -> None:
        with zipfile.ZipFile(output_path, "w") as zf:
            zf.writestr("lesson.json", "{}")

    def validate(self, output_path: str) -> bool:
        return os.path.exists(output_path) and zipfile.is_zipfile(output_path)

    def metadata(self, output_path: str) -> Dict[str, Any]:
        meta = super().metadata(output_path)
        meta["export_type"] = "offline"
        return meta
