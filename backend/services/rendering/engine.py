import os
import json
from typing import Dict, Any, Optional
from services.rendering.factory import RendererFactory
from services.rendering.writers.json_writer import JsonWriter
from services.rendering.schemas import PresentationLayoutModel

class RenderingEngine:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root

    def before_render(self, lesson_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        return lesson_plan_data

    def render(self, lesson_plan_data: Dict[str, Any], renderer_type: str = "deterministic") -> PresentationLayoutModel:
        processed_data = self.before_render(lesson_plan_data)
        renderer = RendererFactory.get_renderer(renderer_type)
        model = renderer.render(processed_data)
        self.after_render(model)
        return model

    def after_render(self, model: PresentationLayoutModel) -> None:
        output_path = os.path.join(self.workspace_root, "lesson_render.json")
        writer = JsonWriter()
        writer.write(model, output_path)

    def execute(self, renderer_type: str = "deterministic") -> PresentationLayoutModel:
        input_path = os.path.join(self.workspace_root, "lesson_plan.json")
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Missing required lesson_plan.json in {self.workspace_root}")
            
        with open(input_path, "r", encoding="utf-8") as f:
            lesson_plan_data = json.load(f)
            
        return self.render(lesson_plan_data, renderer_type)

    def execute_themed_pipeline(self, theme_name: str = "default") -> Dict[str, Any]:
        from services.rendering.slide_builder import SlideBuilder
        from services.rendering.templates import select_template
        from services.rendering.optimization.validator import VisualDesignValidator
        
        lesson_render_path = os.path.join(self.workspace_root, "lesson_render.json")
        if not os.path.exists(lesson_render_path):
            self.execute("deterministic")
            
        builder = SlideBuilder(self.workspace_root)
        presentation = builder.build_presentation(lesson_render_path, theme_name)
        
        slides = presentation.get("slides", [])
        total = len(slides)
        for idx, slide in enumerate(slides):
            tpl = select_template(slide, idx, total)
            slide["template_name"] = tpl
            
        VisualDesignValidator.validate_visuals(presentation, self.workspace_root)
        
        themed_path = os.path.join(self.workspace_root, "lesson_themed.json")
        with open(themed_path, "w", encoding="utf-8") as f:
            json.dump(presentation, f, indent=2)
            
        return presentation
