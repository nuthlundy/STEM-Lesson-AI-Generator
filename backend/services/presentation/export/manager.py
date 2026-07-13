import time
import os
from typing import Dict, Any, List
from services.presentation.export.factory import PresentationExportFactory
from services.presentation.export.metadata import ExportMetadataManager

class PresentationExportManager:
    def __init__(self, factory: PresentationExportFactory = None) -> None:
        self.factory = factory or PresentationExportFactory()
        self.exports_history: List[Dict[str, Any]] = []

    def execute_export(self, export_type: str, session_path: str, output_path: str, workspace_root: str = ".") -> Dict[str, Any]:
        exporter = self.factory.get_exporter(export_type)
        start_time = time.time()
        
        status = "success"
        try:
            exporter.export(session_path, output_path)
            valid = exporter.validate(output_path)
            if not valid:
                status = "invalid"
        except Exception:
            status = "failed"
            
        duration = time.time() - start_time
        meta = exporter.metadata(output_path)
        
        entry = {
            "export_type": export_type,
            "export_status": status,
            "output_filename": os.path.basename(output_path),
            "generation_timestamp": meta.get("generation_timestamp", start_time),
            "export_duration": duration
        }
        
        self.exports_history.append(entry)
        ExportMetadataManager.generate_exports_report(workspace_root, self.exports_history)
        return entry
