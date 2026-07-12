from abc import ABC, abstractmethod
from services.rendering.schemas import PresentationLayoutModel

class BaseWriter(ABC):
    @abstractmethod
    def write(self, model: PresentationLayoutModel, output_path: str) -> None:
        """Writes the presentation layout model to disk."""
        pass
