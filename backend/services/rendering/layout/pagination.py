from typing import Dict, Any

class PaginationTracker:
    def __init__(self, total_slides: int = 0):
        self.total_slides = total_slides
        self.current_slide_index = 0

    def get_slide_number(self) -> int:
        return self.current_slide_index + 1

    def format_footer(self) -> str:
        return f"Slide {self.get_slide_number()} of {self.total_slides}"
