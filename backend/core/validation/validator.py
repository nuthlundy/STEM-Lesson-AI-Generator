from typing import Dict, Any, List
from core.validation.checks import SystemChecks
from core.validation.report import ValidationReporter
from core.artifacts.registry import get_canonical_registry
from core.validation.exceptions import ValidationError

class SystemValidator:
    @staticmethod
    def validate_platform(workspace_root: str = None) -> Dict[str, Any]:
        if not workspace_root:
            workspace_root = get_canonical_registry()._resolver.workspace_root
            
        checks = [
            SystemChecks.check_workspace(workspace_root),
            SystemChecks.check_configuration(),
            SystemChecks.check_plugins(),
            SystemChecks.check_artifacts()
        ]
        
        report = ValidationReporter.generate_report(checks, workspace_root)
        
        if report["status"] == "Critical":
            raise ValidationError("Critical platform validation failures found. Aborting startup.")
            
        return report
