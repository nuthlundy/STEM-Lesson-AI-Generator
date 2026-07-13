from services.presentation.export.interfaces.exporter import ExporterInterface
from typing import Dict, Any

class BasePresentationExporter(ExporterInterface):
    def export(self, session_path: str, output_path: str) -> None:
        pass

    def validate(self, output_path: str) -> bool:
        return True

    def metadata(self, output_path: str) -> Dict[str, Any]:
        import time
        return {
            "output_filename": output_path,
            "generation_timestamp": time.time(),
            "export_duration": 0.1,
            "export_type": "base"
        }
