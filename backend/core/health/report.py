import os
import json
import datetime
from typing import Dict, Any
from core.health.checker import PlatformHealthChecker
from core.artifacts.registry import get_canonical_registry

class PlatformHealthReporter:
    @staticmethod
    def generate_report(workspace_root: str = None) -> Dict[str, Any]:
        if not workspace_root:
            workspace_root = get_canonical_registry()._resolver.workspace_root
            
        data = PlatformHealthChecker.run_health_checks()
        report = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "health": data
        }
        
        os.makedirs(workspace_root, exist_ok=True)
        file_path = os.path.join(workspace_root, "platform_health.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
            
        return report
