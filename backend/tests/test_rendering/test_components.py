import unittest
from services.rendering.components.title import TitleComponent
from services.rendering.components.text import TextComponent
from services.rendering.components.table import TableComponent
from services.rendering.components.figure import FigureComponent
from services.rendering.components.equation import EquationComponent
from services.rendering.components.bullet import BulletComponent
from services.rendering.components.code import CodeComponent
from services.rendering.components.footer import FooterComponent

class TestComponents(unittest.TestCase):
    def test_title_component(self):
        c = TitleComponent("Hello Title")
        self.assertEqual(c.to_dict(), {"type": "title", "text": "Hello Title"})

    def test_text_component(self):
        c = TextComponent("Some text content")
        self.assertEqual(c.to_dict(), {"type": "text", "content": "Some text content"})

    def test_table_component(self):
        c = TableComponent(["Header"], [["Row1"]])
        self.assertEqual(c.to_dict(), {"type": "table", "headers": ["Header"], "rows": [["Row1"]]})

    def test_figure_component(self):
        c = FigureComponent("http://img.png", "Caption")
        self.assertEqual(c.to_dict(), {"type": "figure", "url": "http://img.png", "caption": "Caption"})

    def test_equation_component(self):
        c = EquationComponent("E=mc^2")
        self.assertEqual(c.to_dict(), {"type": "equation", "latex": "E=mc^2"})

    def test_bullet_component(self):
        c = BulletComponent(["Point 1"])
        self.assertEqual(c.to_dict(), {"type": "bullet", "items": ["Point 1"]})

    def test_code_component(self):
        c = CodeComponent("print(1)", "python")
        self.assertEqual(c.to_dict(), {"type": "code", "code": "print(1)", "language": "python"})

    def test_footer_component(self):
        c = FooterComponent(2, 5)
        self.assertEqual(c.to_dict(), {"type": "footer", "slide_num": 2, "total_slides": 5})

if __name__ == "__main__":
    unittest.main()
