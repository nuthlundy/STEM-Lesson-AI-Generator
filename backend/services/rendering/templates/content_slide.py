from services.rendering.templates.base import BaseSlideTemplate

class ContentSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "content_slide"
