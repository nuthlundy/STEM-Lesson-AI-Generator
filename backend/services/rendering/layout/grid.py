from typing import List, Dict, Any

class GridSystem:
    def __init__(self, slide_width: float = 960.0, slide_height: float = 540.0):
        self.slide_width = slide_width
        self.slide_height = slide_height

    def calculate_columns(self, num_columns: int, margins: Any) -> List[Dict[str, float]]:
        available_width = self.slide_width - margins.left - margins.right
        column_width = available_width / num_columns
        
        columns = []
        for i in range(num_columns):
            x_pos = margins.left + (i * column_width)
            columns.append({
                "x": x_pos,
                "y": margins.top,
                "width": column_width,
                "height": self.slide_height - margins.top - margins.bottom
            })
        return columns
