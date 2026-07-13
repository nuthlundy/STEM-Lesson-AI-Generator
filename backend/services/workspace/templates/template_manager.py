import time
import uuid
from typing import List, Dict, Any, Optional
from services.workspace.templates.template import LessonTemplate
from services.workspace.templates.template_store import TemplateStore
from services.workspace.templates.template_validator import TemplateValidator

class TemplateManager:
    def __init__(self, storage_path: str = ".", on_change_callback = None) -> None:
        self.store = TemplateStore(storage_path=storage_path)
        self.templates: List[LessonTemplate] = self.store.load_templates()
        self.on_change_callback = on_change_callback

    def create_template(self, name: str, category: str, description: str, curriculum: str = "NGSS", grades: List[str] = None) -> Optional[LessonTemplate]:
        template_id = str(uuid.uuid4())
        tmpl = LessonTemplate(
            template_id=template_id,
            template_name=name,
            category=category,
            description=description,
            supported_curriculum=curriculum,
            supported_grades=grades or [],
            created_timestamp=time.time()
        )
        if TemplateValidator.validate(tmpl, self.templates):
            self.templates.append(tmpl)
            self.store.save_templates(self.templates)
            if self.on_change_callback:
                self.on_change_callback()
            return tmpl
        return None

    def update_template(self, template_id: str, updates: Dict[str, Any]) -> bool:
        for tmpl in self.templates:
            if tmpl.template_id == template_id:
                cand = LessonTemplate(**{**tmpl.model_dump(), **updates})
                if TemplateValidator.validate(cand, self.templates):
                    for k, v in updates.items():
                        if hasattr(tmpl, k):
                            setattr(tmpl, k, v)
                    self.store.save_templates(self.templates)
                    if self.on_change_callback:
                        self.on_change_callback()
                    return True
        return False

    def delete_template(self, template_id: str) -> bool:
        for i, t in enumerate(self.templates):
            if t.template_id == template_id:
                self.templates.pop(i)
                self.store.save_templates(self.templates)
                if self.on_change_callback:
                    self.on_change_callback()
                return True
        return False

    def list_templates(self) -> List[LessonTemplate]:
        return list(self.templates)

    def apply_template(self, template_id: str, project_id: str) -> bool:
        for tmpl in self.templates:
            if tmpl.template_id == template_id:
                return True
        return False
