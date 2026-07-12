from core.workflow.pipeline import Pipeline
from core.validation.exceptions import ValidationError

class PipelineValidator:
    @staticmethod
    def validate(pipeline: Pipeline) -> None:
        if not pipeline.stages:
            raise ValidationError("Pipeline has no stages defined.")
        # Basic name verification
        if not pipeline.name.strip():
            raise ValidationError("Pipeline name cannot be empty.")
