from services.lesson_planning.interfaces.planner import LessonPlanner
from services.lesson_planning.processors.deterministic import DeterministicLessonPlanner
from services.lesson_planning.processors.gemini_processor import GeminiLessonPlanner
from services.lesson_planning.config import lpe_config
from core.logger import get_logger

logger = get_logger("stem_ai.lpe.factory")

class ProcessorFactory:
    """Factory to load active LessonPlanner based on configuration."""
    @staticmethod
    def get_planner() -> LessonPlanner:
        provider = lpe_config.active_planner_provider.lower()
        if provider == "gemini":
            return GeminiLessonPlanner()
        elif provider == "deterministic":
            return DeterministicLessonPlanner()
        else:
            logger.warning(f"Unknown active_planner_provider '{provider}'. Falling back to deterministic.")
            return DeterministicLessonPlanner()
