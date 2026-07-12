from services.rendering.templates.base import BaseSlideTemplate

class ProcessSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "process_slide"
