from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class LayoutSuggestion(BaseModel):
    suggested_layout: str
    rationale: str

class ImagePlacementSuggestion(BaseModel):
    image_key: str
    position: str # left, right, top, bottom, background
    fit: str # cover, contain

class TableLayoutSuggestion(BaseModel):
    table_key: str
    columns_widths: List[float] = Field(default_factory=list)
    zebra_striping: bool = True

class AnimationSuggestion(BaseModel):
    element_key: str
    animation_type: str # fade, slide, scale
    duration_seconds: float = 0.5

class PresenterNotes(BaseModel):
    talking_points: List[str] = Field(default_factory=list)
    timing_guidelines_seconds: int = 60

class VisualHierarchyScore(BaseModel):
    balance_score: float = 1.0 # 0.0 to 1.0
    whitespace_ratio: float = 0.3 # 0.0 to 1.0
    contrast_ratio: float = 4.5 # minimum recommended WCAG

class AIRenderMetadata(BaseModel):
    layout_suggestions: List[LayoutSuggestion] = Field(default_factory=list)
    image_placement_suggestions: List[ImagePlacementSuggestion] = Field(default_factory=list)
    table_layout_suggestions: List[TableLayoutSuggestion] = Field(default_factory=list)
    animation_suggestions: List[AnimationSuggestion] = Field(default_factory=list)
    presenter_notes: Optional[PresenterNotes] = None
    visual_hierarchy_score: Optional[VisualHierarchyScore] = None
    confidence: float = 1.0

class SlideContent(BaseModel):
    title: str
    points: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    ai_suggestions: Optional[str] = None
    ai_enrichment: Optional[AIRenderMetadata] = None

class PresentationLayoutModel(BaseModel):
    version: str = "1.0"
    layout_type: str = "slides"
    slides: List[SlideContent] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
