from typing import List
from services.subject_intelligence.instructional.schemas import SequenceStep
from services.subject_intelligence.curriculum.schemas import LearningObjective

class LearningSequenceGenerator:
    """Generates sequential steps mapping scheduled concepts to respective learning objectives."""
    
    @staticmethod
    def generate_sequence(scheduled_concepts: List[str], objectives: List[LearningObjective]) -> List[SequenceStep]:
        sequence = []
        for idx, concept in enumerate(scheduled_concepts):
            mapped_objectives = []
            for obj in objectives:
                if any(concept.lower() in mc.lower() for mc in obj.mapped_concepts):
                    mapped_objectives.append(obj.description)
                    
            sequence.append(SequenceStep(
                step_number=idx + 1,
                concept=concept,
                objectives=mapped_objectives,
                estimated_minutes=45
            ))
        return sequence
