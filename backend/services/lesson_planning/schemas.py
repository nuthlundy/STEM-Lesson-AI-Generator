from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from services.lesson_planning.constants import ENGINE_NAME, ENGINE_VERSION, SCHEMA_VERSION

class LessonSection(BaseModel):
    title: str
    duration_minutes: int
    objectives: List[str] = Field(default_factory=list)
    description: str

class Transition(BaseModel):
    from_section: str
    to_section: str
    transition_notes: str

class ValidationReport(BaseModel):
    valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    total_duration_minutes: int

class LessonTimeline(BaseModel):
    sections: List[LessonSection] = Field(default_factory=list)

class DifferentiationBlock(BaseModel):
    learner_profiles: List[str] = Field(default_factory=list)
    accommodations: Dict[str, str] = Field(default_factory=dict)
    intervention_strategies: Dict[str, str] = Field(default_factory=dict)
    enrichment_recommendations: Dict[str, str] = Field(default_factory=dict)

class AssessmentAlignment(BaseModel):
    assessment_objective: str
    lesson_objective_id: str
    bloom_level: str
    curriculum_standard: str
    lesson_section: str
    concept: str

class AssessmentBlueprintItem(BaseModel):
    assessment_type: str  # Formative, Summative, Exit Ticket, Observation, Practical, Project
    topic: str
    weight: float
    target_questions_count: int
    alignment: List[AssessmentAlignment] = Field(default_factory=list)

class AssessmentPlan(BaseModel):
    assessment_blueprint: List[AssessmentBlueprintItem] = Field(default_factory=list)
    bloom_distribution: Dict[str, float] = Field(default_factory=dict)
    question_distribution: Dict[str, int] = Field(default_factory=dict)
    assessment_alignment: List[AssessmentAlignment] = Field(default_factory=list)

class LessonReadiness(BaseModel):
    readiness_score: float
    curriculum_completeness: bool
    assessment_completeness: bool
    timing_validation: bool
    materials_completeness: bool
    details: Dict[str, Any] = Field(default_factory=dict)

class TeacherGuidanceBlock(BaseModel):
    teacher_guidance: str
    materials: List[str] = Field(default_factory=list)
    preparation: List[str] = Field(default_factory=list)
    classroom_management: List[str] = Field(default_factory=list)
    misconceptions: List[str] = Field(default_factory=list)
    reflection_prompts: List[str] = Field(default_factory=list)
    lesson_readiness: LessonReadiness

class LessonPlan(BaseModel):
    engine_name: str = Field(default=ENGINE_NAME)
    engine_version: str = Field(default=ENGINE_VERSION)
    schema_version: str = Field(default=SCHEMA_VERSION)
    generated_at: str
    source_artifacts: Dict[str, Any] = Field(default_factory=dict)
    
    subject: str
    title: str
    lesson_structure: str
    lesson_sections: List[LessonSection] = Field(default_factory=list)
    timeline: List[str] = Field(default_factory=list)
    transitions: List[Transition] = Field(default_factory=list)
    objective_mapping: Dict[str, List[str]] = Field(default_factory=dict)
    validation_report: ValidationReport
    
    # AI Enrichment Fields
    ai_enrichment: Optional[Dict[str, Any]] = None
    teacher_notes: Dict[str, str] = Field(default_factory=dict)
    engagement_suggestions: Dict[str, str] = Field(default_factory=dict)
    pacing_recommendations: Dict[str, str] = Field(default_factory=dict)
    confidence: Optional[float] = None
    
    # Differentiation Fields
    differentiation: Optional[DifferentiationBlock] = None
    learner_profiles: List[str] = Field(default_factory=list)
    accommodations: Dict[str, str] = Field(default_factory=dict)
    intervention_strategies: Dict[str, str] = Field(default_factory=dict)
    enrichment_recommendations: Dict[str, str] = Field(default_factory=dict)
    
    # Assessment Fields
    assessment_plan: Optional[AssessmentPlan] = None
    assessment_blueprint: List[AssessmentBlueprintItem] = Field(default_factory=list)
    bloom_distribution: Dict[str, float] = Field(default_factory=dict)
    question_distribution: Dict[str, int] = Field(default_factory=dict)
    assessment_alignment: List[AssessmentAlignment] = Field(default_factory=list)
    
    # Guidance and Readiness Fields
    teacher_guidance: Optional[str] = None
    materials: List[str] = Field(default_factory=list)
    preparation: List[str] = Field(default_factory=list)
    classroom_management: List[str] = Field(default_factory=list)
    misconceptions: List[str] = Field(default_factory=list)
    reflection_prompts: List[str] = Field(default_factory=list)
    lesson_readiness: Optional[LessonReadiness] = None
    
    model_config = {
        "protected_namespaces": ()
    }
