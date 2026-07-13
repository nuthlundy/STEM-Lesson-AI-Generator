from abc import ABC, abstractmethod
from services.presentation.schemas import PresentationSessionModel

class BasePresentationWriter(ABC):
    @abstractmethod
    def write(self, model: PresentationSessionModel, output_path: str) -> None:
        pass
