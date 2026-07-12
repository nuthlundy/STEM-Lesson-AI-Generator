from abc import abstractmethod
from typing import Dict, Any
from services.rendering.interfaces.renderer import BaseRenderer

class SlideRendererInterface(BaseRenderer):
    @abstractmethod
    def build_slides(self, lesson_plan_data: Dict[str, Any]) -> list:
        """Processes the input data and extracts individual slide items."""
        pass
