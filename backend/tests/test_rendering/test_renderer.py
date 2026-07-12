import unittest
from typing import Dict, Any
from services.rendering.processors.deterministic_renderer import DeterministicRenderer
from services.rendering.processors.gemini_renderer import GeminiRenderer
from services.rendering.schemas import PresentationLayoutModel, SlideContent

class TestRenderers(unittest.TestCase):
    def setUp(self):
        self.lesson_plan_data = {
            "title": "Introduction to Robotics",
            "lesson_sections": [
                {
                    "name": "Warmup",
                    "duration_minutes": 5,
                    "description": "Short video demonstration",
                    "teacher_notes": "Prep video beforehand"
                },
                {
                    "name": "Direct Instruction",
                    "duration_minutes": 15,
                    "description": "Explain robotics laws",
                    "teacher_notes": "Use presentation slides"
                }
            ]
        }

    def test_deterministic_renderer(self):
        renderer = DeterministicRenderer()
        model = renderer.render(self.lesson_plan_data)
        
        self.assertIsInstance(model, PresentationLayoutModel)
        self.assertEqual(model.metadata["title"], "Introduction to Robotics")
        self.assertEqual(len(model.slides), 2)
        self.assertEqual(model.slides[0].title, "Warmup")
        self.assertIn("Duration: 5 mins", model.slides[0].points[0])

    def test_gemini_renderer_enrichment(self):
        renderer = GeminiRenderer()
        model = renderer.render(self.lesson_plan_data)
        
        self.assertIsInstance(model, PresentationLayoutModel)
        self.assertTrue(model.metadata["ai_enriched"])
        self.assertEqual(model.metadata["renderer"], "GeminiRenderer")
        for slide in model.slides:
            self.assertIsNotNone(slide.ai_suggestions)

    def test_rendering_constants(self):
        from services.rendering.constants import DEFAULT_LAYOUT_TYPE, SUPPORTED_FORMATS
        self.assertEqual(DEFAULT_LAYOUT_TYPE, "slides")
        self.assertIn("pptx", SUPPORTED_FORMATS)

    def test_slide_content_pydantic_schema(self):
        s = SlideContent(title="Title", points=["P1"], notes="N1")
        self.assertEqual(s.title, "Title")
        self.assertEqual(s.points, ["P1"])

    def test_presentation_layout_model_schema(self):
        m = PresentationLayoutModel(version="1.1", layout_type="slides", slides=[])
        self.assertEqual(m.version, "1.1")
        self.assertEqual(m.layout_type, "slides")

    def test_empty_lesson_sections_rendering(self):
        renderer = DeterministicRenderer()
        model = renderer.render({"title": "Empty", "lesson_sections": []})
        self.assertEqual(len(model.slides), 0)

    def test_document_renderer_custom_subclass(self):
        from services.rendering.interfaces.document_renderer import DocumentRendererInterface
        
        class MockDocRenderer(DocumentRendererInterface):
            def build_document_sections(self, lesson_plan_data: Dict[str, Any]) -> list:
                return [{"title": "Doc Section"}]
            def render(self, lesson_plan_data: Dict[str, Any]) -> PresentationLayoutModel:
                return PresentationLayoutModel(
                    version="1.0",
                    layout_type="document",
                    slides=[],
                    metadata={"title": "Doc"}
                )
                
        r = MockDocRenderer()
        self.assertEqual(r.build_document_sections({}), [{"title": "Doc Section"}])
        model = r.render({})
        self.assertEqual(model.layout_type, "document")

    def test_rendering_config_defaults(self):
        from services.rendering.config import RenderingConfig
        cfg = RenderingConfig()
        self.assertEqual(cfg.theme, "modern")
        self.assertEqual(cfg.default_format, "html")

    def test_rendering_types_exceptions(self):
        from services.rendering.types import RenderingError, UnsupportedFormatError, LayoutError
        with self.assertRaises(RenderingError):
            raise UnsupportedFormatError("Bad format")
        with self.assertRaises(RenderingError):
            raise LayoutError("Bad layout")

    def test_slide_content_notes_defaults(self):
        s = SlideContent(title="Test Slide")
        self.assertIsNone(s.notes)
        self.assertIsNone(s.ai_suggestions)

    def test_presentation_layout_metadata_defaults(self):
        m = PresentationLayoutModel()
        self.assertEqual(m.metadata, {})

if __name__ == "__main__":
    unittest.main()
