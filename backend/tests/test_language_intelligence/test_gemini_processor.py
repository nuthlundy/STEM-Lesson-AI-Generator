import unittest
import asyncio
import sys
from unittest.mock import AsyncMock, MagicMock, patch

mock_genai_module = MagicMock()
sys.modules['google.generativeai'] = mock_genai_module

from services.language_intelligence.processors.gemini_processor import GeminiProcessor
from services.language_intelligence.interfaces import SemanticRole

class TestGeminiProcessor(unittest.TestCase):
    @patch('services.language_intelligence.processors.gemini_processor.HAS_GENAI', False)
    @patch('services.language_intelligence.config.lie_config.gemini_api_key', '')
    def test_fallback_when_not_configured(self):
        processor = GeminiProcessor()
        raw = "This is raw."
        result = asyncio.run(processor.process(raw))
        
        self.assertEqual(result.processing_provider, "deterministic")
        self.assertEqual(result.semantic_role, SemanticRole.UNKNOWN)
        self.assertIsNone(result.confidence)
        
    @patch('services.language_intelligence.processors.gemini_processor.HAS_GENAI', True)
    @patch('services.language_intelligence.processors.gemini_processor.lie_config.gemini_api_key', 'test_key')
    @patch('services.language_intelligence.processors.gemini_processor.genai')
    def test_gemini_processing_success(self, mock_genai):
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"semantic_role": "definition", "keywords": ["test"], "confidence": 0.99}'
        mock_model.generate_content_async = AsyncMock(return_value=mock_response)
        mock_genai.GenerativeModel.return_value = mock_model
        
        processor = GeminiProcessor()
        
        raw = "This defines something."
        result = asyncio.run(processor.process(raw))
        
        self.assertEqual(result.processing_provider, "gemini")
        self.assertEqual(result.semantic_role, SemanticRole.DEFINITION)
        self.assertEqual(result.confidence, 0.99)
        self.assertEqual(result.keywords, ["test"])

if __name__ == "__main__":
    unittest.main()
