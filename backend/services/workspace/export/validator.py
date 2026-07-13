from typing import Dict, Any

class ExportValidator:
    @staticmethod
    def validate_completeness(data: Dict[str, Any], required_keys: list) -> bool:
        for key in required_keys:
            if key not in data:
                return False
        return True

    @staticmethod
    def validate_metadata(data: Dict[str, Any]) -> bool:
        return "version" in data or "workspace_id" in data or "project_id" in data
