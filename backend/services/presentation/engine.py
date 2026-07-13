import os
import json
import uuid
from typing import Dict, Any, Optional
from services.presentation.config import PresentationConfig
from services.presentation.schemas import PresentationSessionModel, PresentationSlideSession
from services.presentation.types import PresentationNotFoundError
from services.presentation.writers.json_writer import JsonPresentationWriter
from services.presentation.navigation.controller import NavigationController
from services.presentation.timing.timer import PresentationTimer
from services.presentation.session import PresentationSessionBuilder

class PresentationEngine:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self._active_session: Optional[PresentationSessionModel] = None
        self._initialized = False
        self.navigation_controller: Optional[NavigationController] = None
        self.timer: Optional[PresentationTimer] = None

    def initialize(self) -> None:
        self._initialized = True
        self.navigation_controller = NavigationController()
        self.timer = PresentationTimer()
        self.timer.start()

    def before_present(self, presentation_path: str) -> None:
        if not os.path.exists(presentation_path):
            raise PresentationNotFoundError(f"PowerPoint file not found: {presentation_path}")

    def present(self, presentation_path: str, config: Optional[PresentationConfig] = None, presenter_type: str = "deterministic") -> PresentationSessionModel:
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
        
        temp_session_path = os.path.join(self.workspace_root, "presentation_session.json")
        writer = JsonPresentationWriter()
        writer.write(session, temp_session_path)

        from services.presentation.factory import PresentationPresenterFactory
        presenter = PresentationPresenterFactory.get_presenter(presenter_type)
        session = presenter.present(temp_session_path)
        
        self.after_present(session)
        return session

    def after_present(self, session: PresentationSessionModel) -> None:
        output_path = os.path.join(self.workspace_root, "presentation_session.json")
        writer = JsonPresentationWriter()
        writer.write(session, output_path)
        
        if self._initialized and self.navigation_controller and self.timer:
            PresentationSessionBuilder.build_delivery_session(
                workspace_root=self.workspace_root,
                navigation=self.navigation_controller,
                timer=self.timer,
                metadata=session.metadata
            )

    def process(self, presentation_path: str, config: Optional[PresentationConfig] = None, presenter_type: str = "deterministic") -> PresentationSessionModel:
        if not self._initialized:
            self.initialize()
        self._active_session = self.present(presentation_path, config, presenter_type)
        return self._active_session

    def shutdown(self) -> None:
        if self.timer:
            self.timer.stop()
        self._active_session = None
        self._initialized = False
        self.navigation_controller = None
        self.timer = None
