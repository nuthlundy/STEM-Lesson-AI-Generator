from services.rendering.templates.title_slide import TitleSlideTemplate
from services.rendering.templates.content_slide import ContentSlideTemplate
from services.rendering.templates.image_slide import ImageSlideTemplate
from services.rendering.templates.table_slide import TableSlideTemplate
from services.rendering.templates.comparison_slide import ComparisonSlideTemplate
from services.rendering.templates.timeline_slide import TimelineSlideTemplate
from services.rendering.templates.process_slide import ProcessSlideTemplate
from services.rendering.templates.summary_slide import SummarySlideTemplate
from services.rendering.templates.quiz_slide import QuizSlideTemplate
from services.rendering.templates.closing_slide import ClosingSlideTemplate

def select_template(slide_data: dict, index: int, total: int) -> str:
    title = slide_data.get("title", "").lower()
    if not title:
        # Check components for title
        for comp in slide_data.get("components", []):
            if comp.get("type") == "title":
                title = comp.get("text", "").lower()
                break
                
    if index == 0:
        return "title_slide"
    if "thank" in title or "closing" in title or index == total - 1:
        return "closing_slide"
        
    components = slide_data.get("components", [])
    for comp in components:
        ctype = comp.get("type")
        if ctype == "table":
            return "table_slide"
        if ctype == "figure":
            return "image_slide"
            
    if "vs" in title or "compare" in title or "comparison" in title:
        return "comparison_slide"
    if "timeline" in title or "history" in title:
        return "timeline_slide"
    if "process" in title or "steps" in title:
        return "process_slide"
    if "summary" in title or "conclusion" in title:
        return "summary_slide"
    if "quiz" in title or "question" in title:
        return "quiz_slide"
        
    return "content_slide"
