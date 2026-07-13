from typing import List, Dict, Any
from services.presentation.schemas import PresentationSessionModel

class ValidationChecks:
    @staticmethod
    def check_slide_sequence(session: PresentationSessionModel) -> List[str]:
        errors = []
        indices = [s.slide_index for s in session.slides]
        if indices != list(range(len(session.slides))):
            errors.append("Slide indices are out of order or discontinuous.")
        return errors

    @staticmethod
    def check_missing_presenter_notes(session: PresentationSessionModel) -> List[str]:
        warnings = []
        for s in session.slides:
            if not s.speaker_notes or not s.speaker_notes.strip():
                warnings.append(f"Slide {s.slide_index} is missing speaker notes.")
        return warnings

    @staticmethod
    def check_missing_objectives(session: PresentationSessionModel) -> List[str]:
        warnings = []
        if "objectives" not in session.metadata:
            warnings.append("Presentation metadata is missing learning objectives.")
        return warnings

    @staticmethod
    def check_export_integrity(session: PresentationSessionModel) -> List[str]:
        return []

    @staticmethod
    def check_navigation_consistency(session: PresentationSessionModel) -> List[str]:
        return []
