from services.rendering.templates.base import BaseSlideTemplate

class TimelineSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "timeline_slide"
