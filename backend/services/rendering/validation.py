from typing import Dict, Any

class RenderingValidationError(Exception):
    pass

class SlideValidator:
    @staticmethod
    def validate_slide(slide_data: Dict[str, Any], index: int) -> None:
        title = slide_data.get("title", "")
        if not title:
            raise RenderingValidationError(f"Slide {index} is missing a title.")
            
        points = slide_data.get("points", [])
        if not points and not slide_data.get("notes", ""):
            raise RenderingValidationError(f"Slide {index} is empty (no points or notes).")
            
        # Overflow detection: warn or error if too many bullet points
        if len(points) > 10:
            raise RenderingValidationError(f"Slide {index} has content overflow (too many bullet points).")
