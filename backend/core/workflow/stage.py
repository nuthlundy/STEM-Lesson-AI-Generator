from pydantic import BaseModel, Field
from typing import List
from core.workflow.state import StageStatus

class WorkflowStage(BaseModel):
    """Pydantic model representing a single step/stage in a workflow execution."""
    stage_id: str
    stage_name: str
    engine_name: str
    status: StageStatus = Field(default=StageStatus.PENDING)
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    execution_time: float = 0.0
    errors: List[str] = Field(default_factory=list)
    
    model_config = {
        "protected_namespaces": ()
    }
