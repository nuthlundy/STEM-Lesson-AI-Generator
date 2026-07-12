from services.rendering.templates.base import BaseSlideTemplate

class TableSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "table_slide"
