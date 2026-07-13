from services.presentation.schemas import PresentationSessionModel
from typing import List

class AccessibilityCheck:
    @staticmethod
    def analyze(session: PresentationSessionModel) -> List[str]:
        issues = []
        for s in session.slides:
            if len(s.title or "") < 3:
                issues.append(f"Slide {s.slide_index} title is too short for accessibility tools.")
        return issues
