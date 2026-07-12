from abc import abstractmethod
from typing import Dict, Any
from services.rendering.interfaces.renderer import BaseRenderer

class DocumentRendererInterface(BaseRenderer):
    @abstractmethod
    def build_document_sections(self, lesson_plan_data: Dict[str, Any]) -> list:
        """Processes the input data and extracts individual document sections."""
        pass
