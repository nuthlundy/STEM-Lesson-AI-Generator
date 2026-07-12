from services.rendering.interfaces.renderer import BaseRenderer
from services.rendering.processors.deterministic_renderer import DeterministicRenderer
from services.rendering.processors.gemini_renderer import GeminiRenderer

class RendererFactory:
    @staticmethod
    def get_renderer(renderer_type: str = "deterministic") -> BaseRenderer:
        if renderer_type == "gemini":
            return GeminiRenderer()
        return DeterministicRenderer()
