from typing import Dict
from services.lesson_planning.differentiation.profiles import LearnerProfiles

class Accommodations:
    @staticmethod
    def get_default_accommodations() -> Dict[str, str]:
        return {
            LearnerProfiles.BELOW_GRADE: "Provide printed templates and mathematical reference sheets.",
            LearnerProfiles.ON_GRADE: "Standard classroom facilities and cooperative tables.",
            LearnerProfiles.ABOVE_GRADE: "Access to advanced simulation toolkits and coding consoles.",
            LearnerProfiles.ELL: "Visual dictionaries, translated glossaries, and extended reading time.",
            LearnerProfiles.SEN: "Audio description devices, print enlargers, and adaptive keyboards.",
            LearnerProfiles.GIFTED: "Advanced laboratory apparatus or sandbox modeling toolkits."
        }
