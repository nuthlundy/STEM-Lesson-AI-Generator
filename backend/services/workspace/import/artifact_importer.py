import os
import json
from typing import Dict, Any

class ArtifactImporter:
    @staticmethod
    def import_artifact_data(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Artifact file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
