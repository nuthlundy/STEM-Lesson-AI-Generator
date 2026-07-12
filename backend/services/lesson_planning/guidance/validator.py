from typing import List, Dict, Any
from services.lesson_planning.schemas import LessonReadiness

class LessonReadinessValidator:
    """Evaluates and builds readiness reports based on standard parameters."""
    
    @staticmethod
    def evaluate_readiness(
        has_objectives: bool,
        has_assessment: bool,
        is_timing_valid: bool,
        has_materials: bool,
        extra_details: Dict[str, Any] = None
    ) -> LessonReadiness:
        score = 0.0
        if has_objectives:
            score += 0.30
        if has_assessment:
            score += 0.30
        if is_timing_valid:
            score += 0.20
        if has_materials:
            score += 0.20
            
        return LessonReadiness(
            readiness_score=round(score, 2),
            curriculum_completeness=has_objectives,
            assessment_completeness=has_assessment,
            timing_validation=is_timing_valid,
            materials_completeness=has_materials,
            details=extra_details or {}
        )
