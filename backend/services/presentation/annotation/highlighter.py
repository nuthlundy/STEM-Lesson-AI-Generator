from typing import List, Tuple

class Highlighter:
    def __init__(self, color: str = "#FFFF00", opacity: float = 0.5) -> None:
        self.color = color
        self.opacity = opacity
        self.regions: List[List[Tuple[float, float]]] = []

    def add_highlight(self, region: List[Tuple[float, float]]) -> None:
        self.regions.append(region)
