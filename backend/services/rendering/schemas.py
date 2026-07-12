from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SlideContent(BaseModel):
    title: str
    points: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    ai_suggestions: Optional[str] = None

class PresentationLayoutModel(BaseModel):
    version: str = "1.0"
    layout_type: str = "slides"
    slides: List[SlideContent] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
