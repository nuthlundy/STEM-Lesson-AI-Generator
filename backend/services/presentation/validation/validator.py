from services.presentation.schemas import PresentationSessionModel
from services.presentation.validation.pipeline import ValidationPipeline
from typing import Dict, Any

class PresentationValidator:
    def __init__(self) -> None:
        self.pipeline = ValidationPipeline()

    def validate_session(self, session: PresentationSessionModel, workspace_root: str) -> Dict[str, Any]:
        return self.pipeline.run(session, workspace_root)
