import unittest
from services.rendering.factory import RendererFactory
from services.rendering.processors.deterministic_renderer import DeterministicRenderer
from services.rendering.processors.gemini_renderer import GeminiRenderer

class TestRendererFactory(unittest.TestCase):
    def test_factory_deterministic(self):
        renderer = RendererFactory.get_renderer("deterministic")
        self.assertIsInstance(renderer, DeterministicRenderer)

    def test_factory_gemini(self):
        renderer = RendererFactory.get_renderer("gemini")
        self.assertIsInstance(renderer, GeminiRenderer)

    def test_factory_default(self):
        renderer = RendererFactory.get_renderer("unknown")
        self.assertIsInstance(renderer, DeterministicRenderer)

if __name__ == "__main__":
    unittest.main()
