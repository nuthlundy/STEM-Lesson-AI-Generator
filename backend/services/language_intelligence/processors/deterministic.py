import string
from services.language_intelligence.processors.base import LanguageProcessor
from services.language_intelligence.interfaces import LinguisticMetadata, SemanticRole
from services.language_intelligence.utils.text_cleaner import TextCleaner
from services.language_intelligence.config import lie_config

class DeterministicProcessor(LanguageProcessor):
    def _detect_language(self, text: str) -> str:
        """Simple deterministic heuristic for language detection based on character sets."""
        if not text:
            return lie_config.default_language
            
        ascii_count = sum(1 for c in text if c in string.printable)
        if ascii_count / len(text) > 0.8:
            return "en"
        return "unknown"

    async def process(self, original_text: str, cleaned_text: str = "") -> LinguisticMetadata:
        """
        Runs deterministic text cleaning and language detection.
        Assigns SemanticRole.UNKNOWN and null confidence since it does not perform semantic inference.
        """
        if not cleaned_text:
            cleaned_text = TextCleaner.clean_text(original_text)
            
        lang = self._detect_language(cleaned_text)
        
        return LinguisticMetadata(
            original_text=original_text,
            cleaned_text=cleaned_text,
            semantic_role=SemanticRole.UNKNOWN,
            keywords=[],
            language=lang,
            confidence=None,
            processing_provider="deterministic",
            model_version=None
        )
