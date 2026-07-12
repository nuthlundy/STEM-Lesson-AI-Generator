import os
import json
import datetime
from typing import Dict, Any
from core.artifacts.registry import get_canonical_registry
from core.config.registry import get_canonical_config_registry

class PlatformDocGenerator:
    @staticmethod
    def generate_summary(workspace_root: str = None) -> Dict[str, Any]:
        if not workspace_root:
            workspace_root = get_canonical_registry()._resolver.workspace_root
            
        artifacts = [art.artifact_id for art in get_canonical_registry().list()]
        providers = [p.provider_type for p in get_canonical_config_registry().list_providers()]
        
        summary = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "metadata": {
                "version": "1.0.0",
                "environment": "production"
            },
            "registered_artifacts": artifacts,
            "registered_providers": providers,
            "registered_plugins": [],
            "supported_engines": [
                "Document Intelligence Engine",
                "Subject Intelligence Engine",
                "Lesson Planning Engine"
            ]
        }
        
        os.makedirs(workspace_root, exist_ok=True)
        file_path = os.path.join(workspace_root, "platform_summary.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
            
        return summary
