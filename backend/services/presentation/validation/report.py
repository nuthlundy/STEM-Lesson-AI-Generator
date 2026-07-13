import json
import os
from typing import Dict, Any, List

class ValidationReport:
    @staticmethod
    def generate_report(workspace_root: str, errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        report = {
            "validation_status": "passed" if not errors else "failed",
            "errors": errors,
            "warnings": warnings,
            "recommendations": ["Add presenter notes where missing."] if warnings else []
        }
        output_path = os.path.join(workspace_root, "presentation_validation.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return report
