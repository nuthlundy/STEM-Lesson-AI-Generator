class LessonPlanningError(Exception):
    """Base exception for Lesson Planning Engine."""
    pass

class PlanningFailedError(LessonPlanningError):
    """Raised when lesson plan generation fails."""
    pass

class ConfigurationError(LessonPlanningError):
    """Raised when planning config parameters are missing or incorrect."""
    pass
