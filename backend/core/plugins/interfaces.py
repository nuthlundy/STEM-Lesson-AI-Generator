from abc import abstractmethod
from typing import Dict, Any
from core.plugins.plugin import BasePlugin

class AIProviderPlugin(BasePlugin):
    """Interface for custom AI generation providers (e.g. OpenAI, Claude)."""
    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """Generates response text from the AI model."""
        pass

class RenderingPlugin(BasePlugin):
    """Interface for visual HTML/PDF/PowerPoint exporters."""
    @abstractmethod
    def render(self, lesson_plan_data: Dict[str, Any], output_format: str) -> bytes:
        """Renders the lesson plan payload into targeted formats (pdf, pptx, html)."""
        pass

class LmsExportPlugin(BasePlugin):
    """Interface for exporting content to LMS providers (Canvas, Google Classroom)."""
    @abstractmethod
    def export_to_lms(self, lesson_plan_data: Dict[str, Any], target_lms: str) -> bool:
        """Publishes the course material directly to the LMS destination."""
        pass

class AssessmentPlugin(BasePlugin):
    """Interface for specialized assessment generators (quiz platforms, rubrics)."""
    @abstractmethod
    def generate_rubric(self, learning_objectives: list) -> Dict[str, Any]:
        """Generates rubrics for given list of learning objectives."""
        pass
