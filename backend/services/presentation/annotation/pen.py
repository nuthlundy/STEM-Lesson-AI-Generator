from typing import List, Tuple

class DrawingPen:
    def __init__(self, color: str = "#FF0000", width: float = 2.0) -> None:
        self.color = color
        self.width = width
        self.strokes: List[List[Tuple[float, float]]] = []

    def add_stroke(self, stroke: List[Tuple[float, float]]) -> None:
        self.strokes.append(stroke)
