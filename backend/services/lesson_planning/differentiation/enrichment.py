from typing import Dict
from services.lesson_planning.differentiation.profiles import LearnerProfiles

class Enrichment:
    @staticmethod
    def get_default_enrichment() -> Dict[str, str]:
        return {
            LearnerProfiles.BELOW_GRADE: "Encourage connections to simple real-world scenarios.",
            LearnerProfiles.ON_GRADE: "Peer tutoring opportunities for master concepts.",
            LearnerProfiles.ABOVE_GRADE: "Independently write algorithm proofs or research projects.",
            LearnerProfiles.ELL: "Language-independent diagrams illustrating physical mechanics.",
            LearnerProfiles.SEN: "Tactile models showcasing geometric shapes.",
            LearnerProfiles.GIFTED: "Develop open-ended extensions or advanced algorithm designs."
        }
