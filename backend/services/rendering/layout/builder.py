from typing import Dict, Any, List
from services.rendering.layout.spacing import Margins
from services.rendering.layout.grid import GridSystem
from services.rendering.layout.pagination import PaginationTracker

class LayoutBuilder:
    def __init__(self, width: float = 960.0, height: float = 540.0):
        self.margins = Margins()
        self.grid = GridSystem(width, height)
        self.tracker = PaginationTracker()

    def build_slide_layout(self, num_columns: int = 1) -> Dict[str, Any]:
        columns = self.grid.calculate_columns(num_columns, self.margins)
        return {
            "margins": {
                "top": self.margins.top,
                "bottom": self.margins.bottom,
                "left": self.margins.left,
                "right": self.margins.right
            },
            "columns": columns,
            "slide_number": self.tracker.get_slide_number()
        }
