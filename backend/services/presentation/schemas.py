from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class PresentationSlideSession(BaseModel):
    slide_index: int
    title: str
    speaker_notes: str = ""
    duration_allocated_seconds: int = 300

class PresentationSessionModel(BaseModel):
    session_id: str
    presentation_path: str
    duration_seconds: int
    slides: List[PresentationSlideSession] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
