from pydantic import BaseModel, Field
from typing import List, Optional
from core.workflow.stage import WorkflowStage
from core.workflow.state import WorkflowStatus

class WorkflowExecution(BaseModel):
    """Pydantic model tracking the execution details of a workflow run."""
    workflow_id: str
    pipeline_name: str
    stages: List[WorkflowStage] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)
    started_at: str
    finished_at: Optional[str] = None
    execution_time: float = 0.0
    status: WorkflowStatus = Field(default=WorkflowStatus.PENDING)
    
    model_config = {
        "protected_namespaces": ()
    }
