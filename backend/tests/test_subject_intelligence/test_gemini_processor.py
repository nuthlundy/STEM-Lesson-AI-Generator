import unittest
import asyncio
import sys
from unittest.mock import AsyncMock, MagicMock, patch

# Mock google.generativeai module
mock_genai_module = MagicMock()
sys.modules['google.generativeai'] = mock_genai_module

from services.subject_intelligence.processors.gemini_processor import GeminiSubjectProcessor
from services.subject_intelligence.constants import STEMSubject

class TestGeminiSubjectProcessor(unittest.TestCase):
    def setUp(self):
        # Clear cache between runs
        GeminiSubjectProcessor._cache.clear()

    @patch('services.subject_intelligence.processors.gemini_processor.HAS_GENAI', False)
    def test_fallback_when_not_configured(self):
        processor = GeminiSubjectProcessor()
        text = "This is a physics formula about gravity."
        result = asyncio.run(processor.process(text))
        
        # Fallback to deterministic
        self.assertEqual(result.subject, STEMSubject.PHYSICS)
        self.assertEqual(result.processing_provider, "deterministic")
        self.assertIsNone(result.ai_enrichment)

    @patch('services.subject_intelligence.processors.gemini_processor.HAS_GENAI', True)
    @patch('services.subject_intelligence.processors.gemini_processor.sie_config.gemini_api_key', 'test_key')
    @patch('services.subject_intelligence.processors.gemini_processor.genai')
    def test_gemini_enrichment_success_and_cache(self, mock_genai):
        mock_model = MagicMock()
        mock_response = MagicMock()
        
        # CS text (triggers General Computer Science topic)
        text = "This will compile."
        
        # AI returns Chemistry
        mock_response.text = '{"subject": "chemistry", "subject_confidence": 0.9, "topic": "Organic Chemistry", "topic_confidence": 0.8, "difficulty": "hard", "difficulty_confidence": 0.9, "vocabulary": ["carbon"], "vocabulary_confidence": 0.8, "prerequisites": ["elements"], "prerequisites_confidence": 0.7}'
        mock_model.generate_content_async = AsyncMock(return_value=mock_response)
        mock_genai.GenerativeModel.return_value = mock_model
        
        processor = GeminiSubjectProcessor()
        result = asyncio.run(processor.process(text))
        
        # Verify deterministic subject remains primary
        self.assertEqual(result.subject, STEMSubject.COMPUTER_SCIENCE)
        
        # Verify AI values filled the empty spots
        self.assertEqual(result.topic, "Organic Chemistry")
        self.assertEqual(result.ai_enrichment.difficulty, "hard")
        
        self.assertIsNotNone(result.ai_enrichment)
        self.assertEqual(result.ai_enrichment.subject, STEMSubject.CHEMISTRY)
        
        # Verify caching
        mock_model.generate_content_async.reset_mock()
        result2 = asyncio.run(processor.process(text))
        mock_model.generate_content_async.assert_not_called()
        self.assertEqual(result2.topic, "Organic Chemistry")

if __name__ == "__main__":
    unittest.main()
