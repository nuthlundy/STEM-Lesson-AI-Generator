from typing import Dict
from services.lesson_planning.differentiation.profiles import LearnerProfiles

class DifferentiationStrategies:
    @staticmethod
    def get_default_strategies() -> Dict[str, str]:
        return {
            LearnerProfiles.BELOW_GRADE: "Scaffold lessons using visual aids, explicit modeling, and chunked conceptual steps.",
            LearnerProfiles.ON_GRADE: "Engage in collaborative peer problem solving and group validations.",
            LearnerProfiles.ABOVE_GRADE: "Incorporate student-led explorations and design inquiry scenarios.",
            LearnerProfiles.ELL: "Utilize bilingual vocab blocks, diagram labels, and peer conversation loops.",
            LearnerProfiles.SEN: "Break down instructions, provide tactile prompts, and allow extra testing intervals.",
            LearnerProfiles.GIFTED: "Encourage conceptual proof extensions and open-ended modeling exercises."
        }
