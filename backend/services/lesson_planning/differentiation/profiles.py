from typing import List

class LearnerProfiles:
    """Supported student learner profiles for differentiated instruction."""
    BELOW_GRADE = "Below Grade Level"
    ON_GRADE = "On Grade Level"
    ABOVE_GRADE = "Above Grade Level"
    ELL = "English Language Learners (ELL)"
    SEN = "Students with Special Educational Needs (SEN)"
    GIFTED = "Gifted Learners"
    
    @staticmethod
    def get_all_profiles() -> List[str]:
        return [
            LearnerProfiles.BELOW_GRADE,
            LearnerProfiles.ON_GRADE,
            LearnerProfiles.ABOVE_GRADE,
            LearnerProfiles.ELL,
            LearnerProfiles.SEN,
            LearnerProfiles.GIFTED
        ]
