from typing import List
from services.workspace.templates.template import LessonTemplate

class TemplateValidator:
    SUPPORTED_CURRICULA = ["NGSS", "IB", "CCSS"]

    @staticmethod
    def validate(template: LessonTemplate, existing_templates: List[LessonTemplate]) -> bool:
        if not template.template_name or not template.template_id:
            return False
        if template.supported_curriculum not in TemplateValidator.SUPPORTED_CURRICULA:
            return False
        for t in existing_templates:
            if t.template_id != template.template_id and t.template_name == template.template_name:
                return False
        return True
