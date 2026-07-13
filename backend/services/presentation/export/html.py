from services.presentation.export.base_exporter import BasePresentationExporter
import os
from typing import Dict, Any

class HtmlPresentationExporter(BasePresentationExporter):
    def export(self, session_path: str, output_path: str) -> None:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("<html><body>Interactive Presentation</body></html>")

    def validate(self, output_path: str) -> bool:
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0

    def metadata(self, output_path: str) -> Dict[str, Any]:
        meta = super().metadata(output_path)
        meta["export_type"] = "html"
        return meta
