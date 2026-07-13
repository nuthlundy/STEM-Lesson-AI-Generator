from typing import Dict, Any, List

class RecoveryRepair:
    @staticmethod
    def repair_missing_metadata(data: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
        repaired = dict(data)
        for k, v in defaults.items():
            if k not in repaired:
                repaired[k] = v
        return repaired

    @staticmethod
    def repair_missing_artifacts(root_path: str, expected_files: List[str]) -> List[str]:
        repaired_files = []
        for f in expected_files:
            import os
            file_path = os.path.join(root_path, f)
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("{}")
                repaired_files.append(f)
        return repaired_files
