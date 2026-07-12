from typing import List
from services.subject_intelligence.constants import STEMSubject
from services.subject_intelligence.curriculum.schemas import StandardAlignment
from services.subject_intelligence.curriculum.standards import StandardsAlignmentEngine

class CurriculumMapper:
    """Orchestrates curriculum standards alignment for subjects."""
    @staticmethod
    def map_standards(subject: STEMSubject, concepts: List[str]) -> List[StandardAlignment]:
        return StandardsAlignmentEngine.get_alignments(subject, concepts)
