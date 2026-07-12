from typing import Dict
from services.lesson_planning.differentiation.profiles import LearnerProfiles

class Intervention:
    @staticmethod
    def get_default_intervention() -> Dict[str, str]:
        return {
            LearnerProfiles.BELOW_GRADE: "One-on-one reviews and step-by-step guidance on math/physics equations.",
            LearnerProfiles.ON_GRADE: "Identify minor errors in formulas during peer reviews.",
            LearnerProfiles.ABOVE_GRADE: "Verify code bounds or boundary conditions.",
            LearnerProfiles.ELL: "Pre-teach key terms before starting development stages.",
            LearnerProfiles.SEN: "Task cards splitting the assignment into small actionable items.",
            LearnerProfiles.GIFTED: "Direct to complex concept debugging tasks if ahead of sequence."
        }
