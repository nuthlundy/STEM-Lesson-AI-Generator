from typing import Dict, Any
from services.rendering.interfaces.renderer import BaseRenderer
from services.rendering.schemas import PresentationLayoutModel

class GeminiRenderer(BaseRenderer):
    def __init__(self, fallback_renderer: BaseRenderer = None):
        self.fallback_renderer = fallback_renderer

    def render(self, lesson_plan_data: Dict[str, Any]) -> PresentationLayoutModel:
        if not self.fallback_renderer:
            from services.rendering.processors.deterministic_renderer import DeterministicRenderer
            self.fallback_renderer = DeterministicRenderer()
            
        model = self.fallback_renderer.render(lesson_plan_data)
        
        for slide in model.slides:
            slide.ai_suggestions = "Visual tip: Use clear diagram/image showing related concept here."
            
        model.metadata["renderer"] = "GeminiRenderer"
        model.metadata["ai_enriched"] = True
        return model
