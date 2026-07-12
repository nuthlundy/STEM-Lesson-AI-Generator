import os
import json
from typing import Dict, Any, List
from services.rendering.layout.builder import LayoutBuilder
from services.rendering.themes import get_theme
from services.rendering.components.title import TitleComponent
from services.rendering.components.text import TextComponent
from services.rendering.components.bullet import BulletComponent
from services.rendering.components.footer import FooterComponent
from services.rendering.validation import SlideValidator

class SlideBuilder:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root

    def build_presentation(self, lesson_render_path: str, theme_name: str = "default") -> Dict[str, Any]:
        with open(lesson_render_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        slides_data = data.get("slides", [])
        total_slides = len(slides_data)
        
        theme = get_theme(theme_name)
        theme_styles = theme.get_styles()

        output_slides = []
        layout_builder = LayoutBuilder()
        layout_builder.tracker.total_slides = total_slides

        for idx, slide in enumerate(slides_data):
            layout_builder.tracker.current_slide_index = idx
            layout = layout_builder.build_slide_layout(num_columns=1)
            
            components = []
            title = slide.get("title", "")
            
            SlideValidator.validate_slide(slide, idx)
            
            if title:
                components.append(TitleComponent(title).to_dict())
            
            for pt in slide.get("points", []):
                components.append(BulletComponent([pt]).to_dict())
                
            components.append(FooterComponent(idx + 1, total_slides).to_dict())
            
            output_slides.append({
                "slide_index": idx,
                "layout": layout,
                "theme_styles": theme_styles,
                "components": components,
                "notes": slide.get("notes", ""),
                "ai_suggestions": slide.get("ai_suggestions", ""),
                "ai_enrichment": slide.get("ai_enrichment", None)
            })

        output_model = {
            "version": "1.0",
            "theme_name": theme_name,
            "slides": output_slides,
            "metadata": data.get("metadata", {})
        }

        output_path = os.path.join(self.workspace_root, "lesson_slides.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_model, f, indent=2)

        return output_model
