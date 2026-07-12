class PromptRepository:
    LAYOUT_ENRICHMENT_PROMPT = """
    Analyze the following slide content and suggest visual layouts, image placements, and hierarchy adjustments:
    Slide Title: {title}
    Slide Points: {points}
    """
    
    @classmethod
    def get_prompt(cls, key: str) -> str:
        if key == "layout":
            return cls.LAYOUT_ENRICHMENT_PROMPT
        return ""
