from typing import Dict, Any, List
from services.rendering.layout.spacing import Margins
from services.rendering.layout.grid import GridSystem
from services.rendering.layout.pagination import PaginationTracker

class LayoutBuilder:
    _cached_columns = {}

    def __init__(self, width: float = 960.0, height: float = 540.0):
        self.margins = Margins()
        self.grid = GridSystem(width, height)
        self.tracker = PaginationTracker()

    def build_slide_layout(self, num_columns: int = 1) -> Dict[str, Any]:
        cache_key = (self.grid.slide_width, self.grid.slide_height, num_columns, self.margins.top, self.margins.bottom, self.margins.left, self.margins.right)

        if cache_key in LayoutBuilder._cached_columns:
            columns = LayoutBuilder._cached_columns[cache_key]
        else:
            columns = self.grid.calculate_columns(num_columns, self.margins)
            LayoutBuilder._cached_columns[cache_key] = columns
            
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

