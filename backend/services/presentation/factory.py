from services.presentation.config import PresentationConfig
from services.presentation.interfaces.presenter import PresenterInterface
from services.presentation.processors.deterministic_presenter import DeterministicPresenter
from services.presentation.processors.gemini_presenter import GeminiPresenter

class PresentationPresenterFactory:
    @staticmethod
    def create_config(duration: int = 3600, view_mode: str = "standard") -> PresentationConfig:
        return PresentationConfig(duration_seconds=duration, view_mode=view_mode)

    @staticmethod
    def get_presenter(presenter_type: str = "deterministic") -> PresenterInterface:
        if presenter_type == "gemini":
            return GeminiPresenter()
        return DeterministicPresenter()
