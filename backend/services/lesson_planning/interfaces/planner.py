from typing import Protocol, Dict, Any
from services.lesson_planning.schemas import LessonPlan

class LessonPlanner(Protocol):
    """Protocol defining the interface for lesson planner modules in Phase 6."""
    async def plan(self, subject: str, context_data: Dict[str, Any]) -> LessonPlan:
        """Generates a LessonPlan based on subject and curriculum/instructional context."""
        ...
