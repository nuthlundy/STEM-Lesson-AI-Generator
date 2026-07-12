import unittest
from services.rendering.utils.cache import RenderingAICache
from services.rendering.utils.merge_engine import RenderingMergeEngine
from services.rendering.processors.gemini_renderer import GeminiRenderer
from services.rendering.schemas import AIRenderMetadata, LayoutSuggestion

class TestAIEnrichment(unittest.TestCase):
    def test_rendering_ai_cache(self):
        cache = RenderingAICache()
        slide = {"title": "Title A", "points": ["P1"]}
        enrichment = {"suggested_layout": "two-column"}
        
        self.assertIsNone(cache.get(slide))
        cache.set(slide, enrichment)
        self.assertEqual(cache.get(slide), enrichment)

    def test_merge_engine_rules(self):
        deterministic = {"title": "Det Title", "points": ["P1"]}
        ai_data = {"title": "AI Title", "points": ["P2"], "notes": "AI Notes"}
        
        merged = RenderingMergeEngine.merge(deterministic, ai_data)
        self.assertEqual(merged["title"], "Det Title")
        self.assertEqual(merged["points"], ["P1", "P2"])
        self.assertEqual(merged["notes"], "AI Notes")

    def test_gemini_renderer_fallback(self):
        renderer = GeminiRenderer()
        lesson_data = {
            "title": "Title",
            "lesson_sections": [{"name": "Sec", "duration_minutes": 10, "description": "Desc"}]
        }
        model = renderer.render(lesson_data)
        self.assertTrue(model.metadata["ai_enriched"])

    def test_schema_enrichment(self):
        meta = AIRenderMetadata(
            layout_suggestions=[LayoutSuggestion(suggested_layout="grid", rationale="better")],
            confidence=0.9
        )
        self.assertEqual(meta.confidence, 0.9)
        self.assertEqual(meta.layout_suggestions[0].suggested_layout, "grid")

if __name__ == "__main__":
    unittest.main()
