import unittest
from services.rendering.layout.spacing import Margins, SpacingTokens
from services.rendering.layout.alignment import TextAlignment
from services.rendering.layout.pagination import PaginationTracker
from services.rendering.layout.grid import GridSystem
from services.rendering.layout.builder import LayoutBuilder

class TestLayoutEngine(unittest.TestCase):
    def test_margins_default(self):
        m = Margins()
        self.assertEqual(m.top, 40.0)
        self.assertEqual(m.bottom, 40.0)

    def test_spacing_tokens(self):
        self.assertEqual(SpacingTokens.LINE_HEIGHT, 1.4)
        self.assertEqual(SpacingTokens.PARAGRAPH_SPACING, 15.0)

    def test_text_alignment(self):
        self.assertEqual(TextAlignment.LEFT, "left")
        self.assertEqual(TextAlignment.CENTER, "center")

    def test_pagination_tracker(self):
        tracker = PaginationTracker(total_slides=5)
        self.assertEqual(tracker.get_slide_number(), 1)
        self.assertEqual(tracker.format_footer(), "Slide 1 of 5")
        tracker.current_slide_index = 2
        self.assertEqual(tracker.get_slide_number(), 3)

    def test_grid_system_columns(self):
        grid = GridSystem()
        margins = Margins(left=50, right=50)
        columns = grid.calculate_columns(num_columns=2, margins=margins)
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0]["width"], 430.0)

    def test_layout_builder_coord(self):
        builder = LayoutBuilder()
        layout = builder.build_slide_layout(num_columns=1)
        self.assertEqual(layout["slide_number"], 1)
        self.assertEqual(len(layout["columns"]), 1)

if __name__ == "__main__":
    unittest.main()
