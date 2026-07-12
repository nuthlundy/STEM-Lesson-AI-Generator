from pydantic import BaseModel, Field
from typing import List, Optional
from services.language_intelligence.interfaces import EnrichedDocumentBlock
from services.document_intelligence.interfaces import ExtractedAsset, ProcessingMetrics, DocumentMetadata
from services.subject_intelligence.schemas import SubjectMetadata
from services.subject_intelligence.constants import ENGINE_NAME, ENGINE_VERSION, SCHEMA_VERSION

class EnrichedSubjectDocumentBlock(EnrichedDocumentBlock):
    subject_metadata: Optional[SubjectMetadata] = None

class SubjectIntelligenceResult(BaseModel):
    metadata: DocumentMetadata
    blocks: List[EnrichedSubjectDocumentBlock] = Field(default_factory=list)
    assets: List[ExtractedAsset] = Field(default_factory=list)
    metrics: ProcessingMetrics = Field(default_factory=ProcessingMetrics)
    
    # Engine output metadata
    engine_name: str = Field(default=ENGINE_NAME)
    engine_version: str = Field(default=ENGINE_VERSION)
    schema_version: str = Field(default=SCHEMA_VERSION)
