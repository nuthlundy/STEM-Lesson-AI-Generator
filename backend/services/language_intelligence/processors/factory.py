import logging
from services.language_intelligence.processors.base import LanguageProcessor
from services.language_intelligence.processors.deterministic import DeterministicProcessor
from services.language_intelligence.processors.gemini_processor import GeminiProcessor
from services.language_intelligence.config import lie_config

logger = logging.getLogger("stem_ai.lie.factory")

class ProcessorFactory:
    """
    Factory to instantiate the appropriate language processor based on configuration.
    Provides an extension point for future providers (OpenAI, Claude, Local).
    """
    @staticmethod
    def get_processor() -> LanguageProcessor:
        provider = lie_config.active_provider.lower()
        
        if provider == "gemini":
            return GeminiProcessor()
        elif provider == "deterministic":
            return DeterministicProcessor()
        else:
            logger.warning(f"Unknown active_provider '{provider}'. Falling back to deterministic.")
            return DeterministicProcessor()
