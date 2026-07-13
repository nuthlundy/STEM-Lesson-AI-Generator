import os
import json
from typing import Dict, Any

class ArtifactExporter:
    @staticmethod
    def export_artifact_data(artifact_data: Dict[str, Any], dest_path: str) -> None:
        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(artifact_data, f, indent=2)
