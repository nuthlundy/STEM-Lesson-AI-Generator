import os
import json
from typing import List
from services.workspace.templates.template import LessonTemplate

class TemplateStore:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.templates_file = os.path.join(storage_path, "templates.json")

    def load_templates(self) -> List[LessonTemplate]:
        if os.path.exists(self.templates_file):
            try:
                with open(self.templates_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [LessonTemplate(**t) for t in data.get("templates", [])]
            except Exception:
                return []
        return []

    def save_templates(self, templates: List[LessonTemplate]) -> None:
        data = {"templates": [t.model_dump() for t in templates]}
        with open(self.templates_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
