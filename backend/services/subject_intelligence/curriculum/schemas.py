from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any

class LearningObjective(BaseModel):
    id: str
    description: str
    bloom_level: Literal["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    mapped_concepts: List[str] = Field(default_factory=list)
    validation_report: Dict[str, Any] = Field(default_factory=dict)

class StandardAlignment(BaseModel):
    standard_code: str
    description: str
    aligned_concepts: List[str] = Field(default_factory=list)

class CurriculumCoverage(BaseModel):
    aligned_standards: List[StandardAlignment] = Field(default_factory=list)
    objectives: List[LearningObjective] = Field(default_factory=list)
    coverage_percentage: float = 0.0
    uncovered_standards: List[str] = Field(default_factory=list)
