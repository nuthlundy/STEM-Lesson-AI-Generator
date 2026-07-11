import unittest
import asyncio
from services.language_intelligence.processors.deterministic import DeterministicProcessor
from services.language_intelligence.interfaces import SemanticRole

class TestDeterministicProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DeterministicProcessor()

    def test_process_english_text(self):
        raw = "This is an   example.\n"
        result = asyncio.run(self.processor.process(raw))
        
        self.assertEqual(result.original_text, raw)
        self.assertEqual(result.cleaned_text, "This is an example.")
        self.assertEqual(result.semantic_role, SemanticRole.UNKNOWN)
        self.assertEqual(result.language, "en")
        self.assertIsNone(result.confidence)
        self.assertEqual(result.processing_provider, "deterministic")

    def test_process_with_pre_cleaned_text(self):
        raw = "Raw text."
        cleaned = "Cleaned text."
        result = asyncio.run(self.processor.process(raw, cleaned))
        
        self.assertEqual(result.original_text, raw)
        self.assertEqual(result.cleaned_text, cleaned)

if __name__ == "__main__":
    unittest.main()
