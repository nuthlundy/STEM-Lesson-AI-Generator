from typing import Dict, Any, List
from services.presentation.schemas import PresentationSessionModel
from services.presentation.validation.checks import ValidationChecks
from services.presentation.validation.report import ValidationReport

class ValidationPipeline:
    def __init__(self) -> None:
        self.checks = [
            ValidationChecks.check_slide_sequence,
            ValidationChecks.check_missing_presenter_notes,
            ValidationChecks.check_missing_objectives,
            ValidationChecks.check_export_integrity,
            ValidationChecks.check_navigation_consistency
        ]

    def run(self, session: PresentationSessionModel, workspace_root: str) -> Dict[str, Any]:
        errors = []
        warnings = []
        for check in self.checks:
            results = check(session)
            for res in results:
                if "missing" in res.lower() or "integrity" in res.lower():
                    warnings.append(res)
                else:
                    errors.append(res)
        return ValidationReport.generate_report(workspace_root, errors, warnings)
