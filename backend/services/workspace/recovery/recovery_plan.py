from pydantic import BaseModel

class RecoveryPlan(BaseModel):
    recovery_id: str
    project_id: str
    checkpoint_id: str
    recovery_strategy: str = "restore_checkpoint"
    execution_status: str = "pending"
