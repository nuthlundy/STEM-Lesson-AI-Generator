from typing import List, Dict, Any
from services.lesson_planning.schemas import AssessmentPlan
from services.lesson_planning.assessment.blueprint import AssessmentBlueprintBuilder
from services.lesson_planning.assessment.taxonomy import BloomTaxonomy
from services.lesson_planning.assessment.weighting import AssessmentWeighting

class AssessmentPlanner:
    """Orchestrates default assessment generation, alignment, and metrics calculation."""
    
    @staticmethod
    def plan_assessment(subject: str, objectives_list: List[Dict[str, Any]], lesson_sections: List[Any]) -> AssessmentPlan:
        blueprint = AssessmentBlueprintBuilder.build_default(subject, objectives_list, lesson_sections)
        
        alignments = []
        for item in blueprint:
            alignments.extend(item.alignment)
            
        bloom_dist = BloomTaxonomy.calculate_distribution(alignments)
        question_dist = AssessmentWeighting.calculate_question_distribution(blueprint)
        
        return AssessmentPlan(
            assessment_blueprint=blueprint,
            bloom_distribution=bloom_dist,
            question_distribution=question_dist,
            assessment_alignment=alignments
        )
