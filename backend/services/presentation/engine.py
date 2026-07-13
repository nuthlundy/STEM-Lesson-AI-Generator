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
from services.presentation.classroom import ClassroomInteractionManager
from services.presentation.annotation import AnnotationManager
from services.presentation.utilities import UtilityManager
from services.presentation.utilities.statistics import AnalyticsManager
from services.presentation.export.factory import PresentationExportFactory
from services.presentation.export.manager import PresentationExportManager
from services.presentation.validation.validator import PresentationValidator
from services.presentation.quality.analyzer import QualityAnalyzer

class PresentationEngine:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self._active_session: Optional[PresentationSessionModel] = None
        self._initialized = False
        self.navigation_controller: Optional[NavigationController] = None
        self.timer: Optional[PresentationTimer] = None
        self.classroom_manager: Optional[ClassroomInteractionManager] = None
        self.annotation_manager: Optional[AnnotationManager] = None
        self.utility_manager: Optional[UtilityManager] = None
        self.analytics_manager: Optional[AnalyticsManager] = None
        self.export_factory: Optional[PresentationExportFactory] = None
        self.export_manager: Optional[PresentationExportManager] = None

    def initialize(self) -> None:
        self._initialized = True
        self.navigation_controller = NavigationController()
        self.timer = PresentationTimer()
        self.timer.start()
        self.classroom_manager = ClassroomInteractionManager()
        self.annotation_manager = AnnotationManager()
        self.utility_manager = UtilityManager()
        self.analytics_manager = AnalyticsManager()
        self.export_factory = PresentationExportFactory()
        
        from services.presentation.export.pdf import PdfPresentationExporter
        from services.presentation.export.html import HtmlPresentationExporter
        from services.presentation.export.web import WebPresentationExporter
        from services.presentation.export.mobile import MobilePresentationExporter
        from services.presentation.export.offline import OfflinePresentationExporter
        from services.presentation.export.print import PrintPresentationExporter
        from services.presentation.export.thumbnails import ThumbnailPresentationExporter
        
        self.export_factory.register("pdf", PdfPresentationExporter)
        self.export_factory.register("html", HtmlPresentationExporter)
        self.export_factory.register("web", WebPresentationExporter)
        self.export_factory.register("mobile", MobilePresentationExporter)
        self.export_factory.register("offline", OfflinePresentationExporter)
        self.export_factory.register("print", PrintPresentationExporter)
        self.export_factory.register("thumbnails", ThumbnailPresentationExporter)
        
        self.export_manager = PresentationExportManager(factory=self.export_factory)

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
        
        validator = PresentationValidator()
        validator.validate_session(session, self.workspace_root)
        
        analyzer = QualityAnalyzer()
        analyzer.analyze_presentation(session, self.workspace_root)
        
        if self._initialized and self.navigation_controller and self.timer:
            PresentationSessionBuilder.build_delivery_session(
                workspace_root=self.workspace_root,
                navigation=self.navigation_controller,
                timer=self.timer,
                metadata=session.metadata,
                ai_metadata=session.ai_metadata
            )
            
        if self._initialized and self.analytics_manager:
            self.analytics_manager.generate_report(self.workspace_root)

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
        self.classroom_manager = None
        self.annotation_manager = None
        self.utility_manager = None
        self.analytics_manager = None
        self.export_factory = None
        self.export_manager = None
