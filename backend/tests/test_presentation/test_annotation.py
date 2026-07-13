import unittest
from services.presentation.annotation.pen import DrawingPen
from services.presentation.annotation.highlighter import Highlighter
from services.presentation.annotation.shapes import ShapesManager
from services.presentation.annotation.whiteboard import Whiteboard
from services.presentation.annotation.pointer import LaserPointer
from services.presentation.annotation import AnnotationManager

class TestPresentationAnnotation(unittest.TestCase):
    def test_drawing_pen(self):
        pen = DrawingPen(color="#0000FF", width=3.0)
        self.assertEqual(pen.color, "#0000FF")
        self.assertEqual(pen.width, 3.0)
        pen.add_stroke([(0.0, 0.0), (1.0, 1.0)])
        self.assertEqual(len(pen.strokes), 1)

    def test_highlighter(self):
        hl = Highlighter(color="#FF00FF", opacity=0.3)
        self.assertEqual(hl.color, "#FF00FF")
        self.assertEqual(hl.opacity, 0.3)
        hl.add_highlight([(0.0, 0.0), (5.0, 5.0)])
        self.assertEqual(len(hl.regions), 1)

    def test_shapes_manager(self):
        shapes = ShapesManager()
        shapes.add_rectangle(0, 0, 10, 10)
        shapes.add_ellipse(5, 5, 2, 2)
        shapes.add_arrow(0, 0, 5, 5)
        shapes.add_line(1, 1, 2, 2)
        self.assertEqual(len(shapes.shapes), 4)

    def test_whiteboard(self):
        wb = Whiteboard()
        wb.create()
        self.assertEqual(len(wb.save()), 1)
        wb.clear()
        self.assertEqual(wb.save(), [{"action": "clear"}])

    def test_laser_pointer(self):
        ptr = LaserPointer()
        self.assertFalse(ptr.visible)
        ptr.set_position(10.5, 20.5)
        ptr.set_visibility(True)
        self.assertTrue(ptr.visible)
        self.assertEqual(ptr.x, 10.5)

    def test_annotation_manager(self):
        mgr = AnnotationManager()
        self.assertIsInstance(mgr.pen, DrawingPen)
        self.assertIsInstance(mgr.highlighter, Highlighter)
        self.assertIsInstance(mgr.shapes, ShapesManager)
        self.assertIsInstance(mgr.whiteboard, Whiteboard)
        self.assertIsInstance(mgr.pointer, LaserPointer)

if __name__ == "__main__":
    unittest.main()
