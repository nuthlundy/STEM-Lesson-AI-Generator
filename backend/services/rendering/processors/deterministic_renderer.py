from typing import Dict, Any
from services.rendering.interfaces.slide_renderer import SlideRendererInterface
from services.rendering.schemas import PresentationLayoutModel, SlideContent

class DeterministicRenderer(SlideRendererInterface):
    def build_slides(self, lesson_plan_data: Dict[str, Any]) -> list:
        slides = []
        sections = lesson_plan_data.get("lesson_sections", [])
        for section in sections:
            slides.append(SlideContent(
                title=section.get("name", "Section"),
                points=[
                    f"Duration: {section.get('duration_minutes', 0)} mins",
                    section.get("description", "")
                ],
                notes=section.get("teacher_notes", "")
            ))
        return slides

    def render(self, lesson_plan_data: Dict[str, Any]) -> PresentationLayoutModel:
        slides = self.build_slides(lesson_plan_data)
        return PresentationLayoutModel(
            version="1.0",
            layout_type="slides",
            slides=slides,
            metadata={
                "title": lesson_plan_data.get("title", "Lesson Slides"),
                "renderer": "DeterministicRenderer"
            }
        )
