from typing import List

class LessonSectionSequencer:
    """Defines the strict ordering of the 10 required lesson sections."""
    REQUIRED_SECTIONS = [
        "Introduction",
        "Learning Objectives",
        "Prior Knowledge",
        "Lesson Development",
        "Guided Practice",
        "Independent Practice",
        "Review",
        "Reflection",
        "Homework Placeholder",
        "Closing"
    ]
    
    @staticmethod
    def get_sequence() -> List[str]:
        return LessonSectionSequencer.REQUIRED_SECTIONS
