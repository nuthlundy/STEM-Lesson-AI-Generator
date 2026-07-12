from typing import List
from services.subject_intelligence.constants import STEMSubject
from services.subject_intelligence.curriculum.schemas import CurriculumCoverage, StandardAlignment, LearningObjective
from services.subject_intelligence.curriculum.standards import StandardsAlignmentEngine

class ConceptCoverageAnalyzer:
    """Analyzes curriculum coverage based on aligned standards and learning objectives."""
    
    @staticmethod
    def analyze(subject: STEMSubject, alignments: List[StandardAlignment], objectives: List[LearningObjective]) -> CurriculumCoverage:
        total_standards = StandardsAlignmentEngine.STANDARDS_REGISTRY.get(subject, [])
        aligned_codes = {a.standard_code for a in alignments}
        
        uncovered = [std.standard_code for std in total_standards if std.standard_code not in aligned_codes]
        
        total_count = len(total_standards)
        coverage_pct = (len(alignments) / total_count * 100.0) if total_count > 0 else 100.0
        
        return CurriculumCoverage(
            aligned_standards=alignments,
            objectives=objectives,
            coverage_percentage=round(coverage_pct, 2),
            uncovered_standards=uncovered
        )
