from services.rendering.templates.base import BaseSlideTemplate

class ClosingSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "closing_slide"
