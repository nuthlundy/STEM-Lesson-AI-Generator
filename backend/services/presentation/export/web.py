from services.presentation.export.base_exporter import BasePresentationExporter
import os
from typing import Dict, Any

class WebPresentationExporter(BasePresentationExporter):
    def export(self, session_path: str, output_path: str) -> None:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write('{"package": "web"}')

    def validate(self, output_path: str) -> bool:
        return os.path.exists(output_path)

    def metadata(self, output_path: str) -> Dict[str, Any]:
        meta = super().metadata(output_path)
        meta["export_type"] = "web"
        return meta
