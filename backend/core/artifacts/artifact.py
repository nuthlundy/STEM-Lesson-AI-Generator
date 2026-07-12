from pydantic import BaseModel, Field
from typing import List, Optional

class Artifact(BaseModel):
    """Pydantic model representing a canonical artifact in the pipeline."""
    artifact_id: str
    artifact_name: str
    schema_version: str
    engine_name: str
    engine_version: str
    file_name: str
    relative_path: str
    produced_by: str
    consumed_by: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    created_at: str
    checksum: str
    description: str
    
    model_config = {
        "protected_namespaces": ()
    }
