from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from services.subject_intelligence.constants import STEMSubject

class AISubjectEnrichment(BaseModel):
    subject: Optional[STEMSubject] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    vocabulary: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    
    # Confidence metrics for individual AI-generated fields
    subject_confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    topic_confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    difficulty_confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    vocabulary_confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    prerequisites_confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)

    model_config = {
        "protected_namespaces": ()
    }

class SubjectMetadata(BaseModel):
    subject: STEMSubject
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    vocabulary: List[str] = Field(default_factory=list)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    prerequisites: List[str] = Field(default_factory=list)
    extracted_formulas: List[str] = Field(default_factory=list)
    validated_formulas: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Nested AI enrichment layer
    ai_enrichment: Optional[AISubjectEnrichment] = None
    
    processing_provider: Literal["deterministic", "gemini"]
    model_version: Optional[str] = None

    model_config = {
        "protected_namespaces": ()
    }
