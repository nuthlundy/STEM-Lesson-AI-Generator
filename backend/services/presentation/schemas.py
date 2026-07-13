from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class PresentationSlideSession(BaseModel):
    slide_index: int
    title: str
    speaker_notes: str = ""
    duration_allocated_seconds: int = 300

class ConfidenceScore(BaseModel):
    score: float = Field(default=1.0, ge=0.0, le=1.0)
    method: str = "deterministic"

class SpeakingSuggestion(BaseModel):
    slide_index: int
    suggestion: str
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore)

class AudienceQuestion(BaseModel):
    slide_index: int
    question: str
    suggested_answer: str
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore)

class DiscussionPrompt(BaseModel):
    slide_index: int
    prompt: str
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore)

class TeachingTip(BaseModel):
    slide_index: int
    tip: str
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore)

class TransitionSuggestion(BaseModel):
    from_slide: int
    to_slide: int
    suggestion: str
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore)

class PresentationAIMetadata(BaseModel):
    speaking_suggestions: List[SpeakingSuggestion] = Field(default_factory=list)
    audience_questions: List[AudienceQuestion] = Field(default_factory=list)
    discussion_prompts: List[DiscussionPrompt] = Field(default_factory=list)
    teaching_tips: List[TeachingTip] = Field(default_factory=list)
    transition_suggestions: List[TransitionSuggestion] = Field(default_factory=list)

class PresentationSessionModel(BaseModel):
    session_id: str
    presentation_path: str
    duration_seconds: int
    slides: List[PresentationSlideSession] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    ai_metadata: Optional[PresentationAIMetadata] = None
