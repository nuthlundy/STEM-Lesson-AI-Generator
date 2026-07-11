from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

class BoundingBox(BaseModel):
    x0: float
    y0: float
    x1: float
    y1: float

class ExtractedAsset(BaseModel):
    asset_id: str
    asset_type: Literal["image", "figure", "table", "equation"]
    file_path: Optional[str] = None
    page_number: int
    bbox: Optional[BoundingBox] = None
    content: Optional[str] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source: Literal["native_pdf", "ocr", "image", "table", "equation", "figure"]
    metadata: Dict = Field(default_factory=dict)

class DocumentBlock(BaseModel):
    block_id: str
    block_type: Literal["heading", "paragraph", "list", "table", "equation", "image_ref"]
    text: str
    page_number: int
    bbox: Optional[BoundingBox] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source: Literal["native_pdf", "ocr", "image", "table", "equation", "figure"]
    metadata: Dict = Field(default_factory=dict)

class ProcessingMetrics(BaseModel):
    progress: float = 0.0
    execution_time: float = 0.0
    warnings: List[str] = Field(default_factory=list)
    recoverable_errors: List[str] = Field(default_factory=list)
    fatal_errors: List[str] = Field(default_factory=list)

class DocumentMetadata(BaseModel):
    job_id: str
    original_filename: str
    total_pages: int
    processing_time_sec: float
    requires_ocr: bool
    schema_version: str = "1.0.0"

class DocumentIntelligenceResult(BaseModel):
    metadata: DocumentMetadata
    blocks: List[DocumentBlock] = Field(default_factory=list)
    assets: List[ExtractedAsset] = Field(default_factory=list)
    metrics: ProcessingMetrics = Field(default_factory=ProcessingMetrics)
