from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from services.document_intelligence.interfaces import (
    DocumentBlock,
    ExtractedAsset,
    ProcessingMetrics,
    DocumentMetadata
)

class SemanticRole(str, Enum):
    DEFINITION = "definition"
    THEOREM = "theorem"
    EXAMPLE = "example"
    EXPLANATION = "explanation"
    UNKNOWN = "unknown"

class LinguisticMetadata(BaseModel):
    original_text: str
    cleaned_text: str
    semantic_role: SemanticRole
    keywords: List[str] = Field(default_factory=list)
    language: str
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    processing_provider: Literal["deterministic", "gemini"]
    model_version: Optional[str] = None
    
    model_config = {
        "protected_namespaces": ()
    }

class EnrichedDocumentBlock(DocumentBlock):
    language_metadata: LinguisticMetadata

class LanguageIntelligenceResult(BaseModel):
    metadata: DocumentMetadata
    blocks: List[EnrichedDocumentBlock] = Field(default_factory=list)
    assets: List[ExtractedAsset] = Field(default_factory=list)
    metrics: ProcessingMetrics = Field(default_factory=ProcessingMetrics)
