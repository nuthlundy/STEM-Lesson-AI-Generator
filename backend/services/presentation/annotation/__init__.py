from services.presentation.annotation.pen import DrawingPen
from services.presentation.annotation.highlighter import Highlighter
from services.presentation.annotation.shapes import ShapesManager
from services.presentation.annotation.whiteboard import Whiteboard
from services.presentation.annotation.pointer import LaserPointer

class AnnotationManager:
    def __init__(self) -> None:
        self.pen = DrawingPen()
        self.highlighter = Highlighter()
        self.shapes = ShapesManager()
        self.whiteboard = Whiteboard()
        self.pointer = LaserPointer()
