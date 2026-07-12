import os
import json
import datetime
from typing import Dict, Any
from core.diagnostics.diagnostics import get_diagnostics_manager
from core.artifacts.registry import get_canonical_registry

class DiagnosticsReporter:
    @staticmethod
    def generate_report(workspace_root: str = None) -> Dict[str, Any]:
        if not workspace_root:
            workspace_root = get_canonical_registry()._resolver.workspace_root
        
        manager = get_diagnostics_manager()
        report_data = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "diagnostics": manager.run_all()
        }
        
        os.makedirs(workspace_root, exist_ok=True)
        file_path = os.path.join(workspace_root, "workflow_diagnostics.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
            
        return report_data
