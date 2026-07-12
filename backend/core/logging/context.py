import threading
import uuid
from typing import Dict, Any, Optional

_local_context = threading.local()

def get_logging_context() -> Dict[str, Any]:
    if not hasattr(_local_context, "data"):
        _local_context.data = {
            "correlation_id": str(uuid.uuid4()),
            "pipeline_id": None,
            "stage_id": None,
            "engine_name": None
        }
    return _local_context.data

def set_logging_context(
    correlation_id: Optional[str] = None,
    pipeline_id: Optional[str] = None,
    stage_id: Optional[str] = None,
    engine_name: Optional[str] = None
) -> None:
    ctx = get_logging_context()
    if correlation_id:
        ctx["correlation_id"] = correlation_id
    if pipeline_id is not None:
        ctx["pipeline_id"] = pipeline_id
    if stage_id is not None:
        ctx["stage_id"] = stage_id
    if engine_name is not None:
        ctx["engine_name"] = engine_name

def clear_logging_context() -> None:
    _local_context.data = {
        "correlation_id": str(uuid.uuid4()),
        "pipeline_id": None,
        "stage_id": None,
        "engine_name": None
    }
