from typing import Protocol
from services.subject_intelligence.schemas import SubjectMetadata

class SubjectProcessor(Protocol):
    """Protocol defining the interface for subject processors in Phase 5."""
    async def process(self, text: str) -> SubjectMetadata:
        """Processes text and returns SubjectMetadata."""
        ...
