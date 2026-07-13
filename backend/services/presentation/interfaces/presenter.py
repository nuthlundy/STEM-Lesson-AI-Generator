from abc import ABC, abstractmethod
from typing import Dict, Any
from services.presentation.schemas import PresentationSessionModel

class PresenterInterface(ABC):
    @abstractmethod
    def before_present(self, session_path: str) -> None:
        pass

    @abstractmethod
    def present(self, session_path: str) -> PresentationSessionModel:
        pass

    @abstractmethod
    def after_present(self, session: PresentationSessionModel) -> None:
        pass
