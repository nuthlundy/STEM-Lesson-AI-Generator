from services.rendering.templates.base import BaseSlideTemplate

class SummarySlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "summary_slide"
