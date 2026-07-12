from services.rendering.templates.base import BaseSlideTemplate

class TitleSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "title_slide"
