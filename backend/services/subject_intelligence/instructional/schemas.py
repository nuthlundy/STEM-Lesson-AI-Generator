from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SequenceStep(BaseModel):
    step_number: int
    concept: str
    objectives: List[str] = Field(default_factory=list)
    estimated_minutes: int = 45

class ReadinessReport(BaseModel):
    ready: bool
    gaps_count: int
    prerequisite_cycles: List[List[str]] = Field(default_factory=list)
    readiness_score: float = 0.0

class InstructionalMetadata(BaseModel):
    total_estimated_minutes: int = 0
    target_audience_profile: str
    instructional_approach: str

class InstructionalModelResult(BaseModel):
    subject: str
    summary: str
    scheduled_concepts: List[str] = Field(default_factory=list)
    sequence: List[SequenceStep] = Field(default_factory=list)
    readiness: ReadinessReport
    gaps: List[str] = Field(default_factory=list)
    metadata: InstructionalMetadata
