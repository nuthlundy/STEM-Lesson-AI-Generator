from services.subject_intelligence.interfaces.processor import SubjectProcessor
from services.subject_intelligence.processors.deterministic import DeterministicSubjectProcessor
from services.subject_intelligence.processors.gemini_processor import GeminiSubjectProcessor
from services.subject_intelligence.config import sie_config
from core.logger import get_logger

logger = get_logger("stem_ai.sie.factory")

class ProcessorFactory:
    """Factory to load active SubjectProcessor based on configuration."""
    @staticmethod
    def get_processor() -> SubjectProcessor:
        provider = sie_config.active_subject_provider.lower()
        if provider == "gemini":
            return GeminiSubjectProcessor()
        elif provider == "deterministic":
            return DeterministicSubjectProcessor()
        else:
            logger.warning(f"Unknown active_subject_provider '{provider}'. Falling back to deterministic.")
            return DeterministicSubjectProcessor()
