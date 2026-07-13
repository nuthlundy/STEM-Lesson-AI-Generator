from typing import List, Dict, Any

class ShapesManager:
    def __init__(self) -> None:
        self.shapes: List[Dict[str, Any]] = []

    def add_rectangle(self, x: float, y: float, w: float, h: float, color: str = "#000000") -> None:
        self.shapes.append({"type": "rectangle", "x": x, "y": y, "w": w, "h": h, "color": color})

    def add_ellipse(self, cx: float, cy: float, rx: float, ry: float, color: str = "#000000") -> None:
        self.shapes.append({"type": "ellipse", "cx": cx, "cy": cy, "rx": rx, "ry": ry, "color": color})

    def add_arrow(self, x1: float, y1: float, x2: float, y2: float, color: str = "#000000") -> None:
        self.shapes.append({"type": "arrow", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "color": color})

    def add_line(self, x1: float, y1: float, x2: float, y2: float, color: str = "#000000") -> None:
        self.shapes.append({"type": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "color": color})
