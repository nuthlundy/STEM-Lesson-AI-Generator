import os
import json
import uuid
from typing import Dict, Any, Optional
from services.presentation.config import PresentationConfig
from services.presentation.schemas import PresentationSessionModel, PresentationSlideSession
from services.presentation.types import PresentationNotFoundError

class PresentationEngine:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root

    def before_present(self, presentation_path: str) -> None:
        if not os.path.exists(presentation_path):
            raise PresentationNotFoundError(f"PowerPoint file not found: {presentation_path}")

    def present(self, presentation_path: str, config: Optional[PresentationConfig] = None) -> PresentationSessionModel:
        self.before_present(presentation_path)
        
        if not config:
            config = PresentationConfig()
            
        slides = [
            PresentationSlideSession(slide_index=0, title="Introduction", speaker_notes="Welcome to the presentation."),
            PresentationSlideSession(slide_index=1, title="Content", speaker_notes="This is the main body.")
        ]
        
        session = PresentationSessionModel(
            session_id=str(uuid.uuid4()),
            presentation_path=presentation_path,
            duration_seconds=config.duration_seconds,
            slides=slides,
            metadata={
                "view_mode": config.view_mode,
                "enable_presenter_view": config.enable_presenter_view
            }
        )
        
        self.after_present(session)
        return session

    def after_present(self, session: PresentationSessionModel) -> None:
        output_path = os.path.join(self.workspace_root, "presentation_session.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(session.model_dump(), f, indent=2)
