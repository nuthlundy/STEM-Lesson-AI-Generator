import unittest
from services.rendering.templates import select_template
from services.rendering.templates.title_slide import TitleSlideTemplate
from services.rendering.templates.content_slide import ContentSlideTemplate

class TestTemplateEngine(unittest.TestCase):
    def test_template_name_properties(self):
        title_tpl = TitleSlideTemplate()
        self.assertEqual(title_tpl.get_template_name(), "title_slide")
        
        content_tpl = ContentSlideTemplate()
        self.assertEqual(content_tpl.get_template_name(), "content_slide")

    def test_auto_selection_title_slide(self):
        slide = {"title": "Intro Slide", "components": []}
        tpl = select_template(slide, index=0, total=5)
        self.assertEqual(tpl, "title_slide")

    def test_auto_selection_closing_slide(self):
        slide = {"title": "Thank You", "components": []}
        tpl = select_template(slide, index=4, total=5)
        self.assertEqual(tpl, "closing_slide")

    def test_auto_selection_table_slide(self):
        slide = {
            "title": "Data",
            "components": [{"type": "table"}]
        }
        tpl = select_template(slide, index=1, total=5)
        self.assertEqual(tpl, "table_slide")

    def test_auto_selection_image_slide(self):
        slide = {
            "title": "Illustration",
            "components": [{"type": "figure"}]
        }
        tpl = select_template(slide, index=2, total=5)
        self.assertEqual(tpl, "image_slide")

    def test_auto_selection_keywords(self):
        slide_vs = {"title": "Python vs Java", "components": []}
        self.assertEqual(select_template(slide_vs, index=1, total=5), "comparison_slide")
        
        slide_quiz = {"title": "Self Assessment Quiz", "components": []}
        self.assertEqual(select_template(slide_quiz, index=2, total=5), "quiz_slide")

if __name__ == "__main__":
    unittest.main()
