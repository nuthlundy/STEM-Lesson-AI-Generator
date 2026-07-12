from typing import Dict, List, Any
from services.lesson_planning.schemas import AssessmentBlueprintItem

class AssessmentWeighting:
    @staticmethod
    def calculate_question_distribution(blueprint: List[AssessmentBlueprintItem]) -> Dict[str, int]:
        dist = {}
        for item in blueprint:
            t = item.assessment_type
            dist[t] = dist.get(t, 0) + item.target_questions_count
        return dist
