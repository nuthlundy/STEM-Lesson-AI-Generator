from typing import List
from services.subject_intelligence.curriculum.schemas import LearningObjective
from services.subject_intelligence.curriculum.bloom import BloomTaxonomyClassifier
from services.subject_intelligence.curriculum.validator import ObjectiveValidator

class LearningObjectiveGenerator:
    """Generates learning objectives for topics and concepts."""
    
    @staticmethod
    def generate_objectives(concepts: List[str]) -> List[LearningObjective]:
        objectives = []
        for idx, concept in enumerate(concepts):
            if idx % 3 == 0:
                desc = f"Explain the fundamental principles of {concept}."
            elif idx % 3 == 1:
                desc = f"Apply formulas related to {concept} to solve standard problems."
            else:
                desc = f"Analyze how {concept} behaves under varying parameters."
                
            bloom_level = BloomTaxonomyClassifier.classify(desc)
            val_report = ObjectiveValidator.validate(desc)
            
            objectives.append(LearningObjective(
                id=f"lo_{idx + 1}",
                description=desc,
                bloom_level=bloom_level,
                mapped_concepts=[concept],
                validation_report=val_report
            ))
            
        return objectives
