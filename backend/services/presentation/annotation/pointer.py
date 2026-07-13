class LaserPointer:
    def __init__(self) -> None:
        self.x = 0.0
        self.y = 0.0
        self.visible = False

    def set_position(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def set_visibility(self, visible: bool) -> None:
        self.visible = visible
