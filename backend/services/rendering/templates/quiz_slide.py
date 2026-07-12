from services.rendering.templates.base import BaseSlideTemplate

class QuizSlideTemplate(BaseSlideTemplate):
    def get_template_name(self) -> str:
        return "quiz_slide"
