from abc import ABC, abstractmethod
from typing import Dict, Any
from services.rendering.schemas import PresentationLayoutModel

class BaseRenderer(ABC):
    @abstractmethod
    def render(self, lesson_plan_data: Dict[str, Any]) -> PresentationLayoutModel:
        """Processes the raw lesson plan payload and builds layout models."""
        pass
