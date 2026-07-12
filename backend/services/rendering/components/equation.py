class EquationComponent:
    def __init__(self, latex: str):
        self.latex = latex
    def to_dict(self) -> dict:
        return {"type": "equation", "latex": self.latex}
