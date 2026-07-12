import re
from core.artifacts.artifact import Artifact
from core.artifacts.exceptions import ValidationError

VALID_ENGINES = {
    "Document Intelligence Engine",
    "Language Intelligence Engine",
    "Subject Intelligence Engine",
    "Lesson Planning Engine"
}

class ArtifactValidator:
    """Validates Artifact metadata fields and rules before registration."""
    
    @staticmethod
    def validate(artifact: Artifact) -> None:
        if not artifact.schema_version or not re.match(r"^v?\d+(\.\d+)*$", artifact.schema_version):
            raise ValidationError(f"Invalid schema version: {artifact.schema_version}. Must match 'vX.Y' pattern.")
            
        if not artifact.checksum or not artifact.checksum.strip():
            raise ValidationError("Checksum cannot be empty.")
            
        if artifact.engine_name not in VALID_ENGINES:
            raise ValidationError(
                f"Invalid engine reference: '{artifact.engine_name}'. Must be one of {VALID_ENGINES}."
            )
            
        if artifact.produced_by not in VALID_ENGINES:
            raise ValidationError(
                f"Invalid producer engine reference: '{artifact.produced_by}'. Must be one of {VALID_ENGINES}."
            )
