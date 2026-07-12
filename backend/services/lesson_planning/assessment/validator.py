from typing import List, Dict, Any
from services.lesson_planning.schemas import AssessmentPlan, AssessmentAlignment
from services.lesson_planning.assessment.taxonomy import BloomTaxonomy

class AssessmentValidator:
    @staticmethod
    def validate(plan: AssessmentPlan) -> bool:
        """Verifies all assessment objective alignments are complete and fully mapped."""
        if not plan.assessment_alignment:
            return False
            
        valid_bloom = set(BloomTaxonomy.get_levels())
        
        for align in plan.assessment_alignment:
            if not align.assessment_objective or not align.assessment_objective.strip():
                return False
            if not align.lesson_objective_id or not align.lesson_objective_id.strip():
                return False
            if align.bloom_level not in valid_bloom:
                return False
            if not align.curriculum_standard or not align.curriculum_standard.strip():
                return False
            if not align.lesson_section or not align.lesson_section.strip():
                return False
            if not align.concept or not align.concept.strip():
                return False
                
        return True
