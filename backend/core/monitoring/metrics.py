from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class StageMetrics(BaseModel):
    stage_id: str
    duration: float = 0.0
    memory_usage_bytes: int = 0
    success_count: int = 0
    failure_count: int = 0
    retry_count: int = 0

class PipelineMetrics(BaseModel):
    pipeline_name: str
    total_duration: float = 0.0
    throughput: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    retry_count: int = 0
    peak_memory_bytes: int = 0
    average_processing_time: float = 0.0
    stage_metrics: Dict[str, StageMetrics] = Field(default_factory=dict)
    health_state: str = "Healthy"

    model_config = {
        "protected_namespaces": ()
    }
