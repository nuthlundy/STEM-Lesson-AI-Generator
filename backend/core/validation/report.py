import os
import json
import datetime
from typing import Dict, Any, List

class ValidationReporter:
    @staticmethod
    def generate_report(checks: List[Dict[str, Any]], workspace_root: str) -> Dict[str, Any]:
        overall_status = "Healthy"
        for check in checks:
            if check["status"] == "Critical":
                overall_status = "Critical"
                break
            elif check["status"] == "Warning" and overall_status != "Critical":
                overall_status = "Warning"
                
        report = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "status": overall_status,
            "checks": checks
        }
        
        os.makedirs(workspace_root, exist_ok=True)
        file_path = os.path.join(workspace_root, "system_validation.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        return report
