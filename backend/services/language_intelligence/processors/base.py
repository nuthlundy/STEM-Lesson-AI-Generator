from typing import Protocol
from services.language_intelligence.interfaces import LinguisticMetadata

class LanguageProcessor(Protocol):
    """Protocol defining the interface for language processors in Phase 4."""
    
    async def process(self, original_text: str, cleaned_text: str) -> LinguisticMetadata:
        """
        Processes text asynchronously and returns enriched linguistic metadata.
        """
        ...
