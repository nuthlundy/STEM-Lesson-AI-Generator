from services.rendering.templates.base import BaseSlideTemplate

class ImageSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "image_slide"
