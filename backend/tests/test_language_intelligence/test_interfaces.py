import unittest
from pydantic import ValidationError
from services.language_intelligence.interfaces import (
    SemanticRole,
    LinguisticMetadata,
    EnrichedDocumentBlock
)

class TestLanguageInterfaces(unittest.TestCase):
    def test_linguistic_metadata_validation(self):
        # Valid deterministic
        meta1 = LinguisticMetadata(
            original_text="This is an  exmaple.",
            cleaned_text="This is an example.",
            semantic_role=SemanticRole.UNKNOWN,
            language="en",
            confidence=None,
            processing_provider="deterministic"
        )
        self.assertEqual(meta1.semantic_role, SemanticRole.UNKNOWN)
        
        # Valid AI
        meta2 = LinguisticMetadata(
            original_text="Define Kinematics.",
            cleaned_text="Define Kinematics.",
            semantic_role=SemanticRole.DEFINITION,
            keywords=["Kinematics"],
            language="en",
            confidence=0.95,
            processing_provider="gemini",
            model_version="gemini-1.5-flash"
        )
        self.assertEqual(meta2.processing_provider, "gemini")

        # Invalid confidence
        with self.assertRaises(ValidationError):
            LinguisticMetadata(
                original_text="Bad",
                cleaned_text="Bad",
                semantic_role=SemanticRole.UNKNOWN,
                language="en",
                confidence=1.5, # > 1.0
                processing_provider="gemini"
            )

    def test_enriched_block_extension(self):
        block = EnrichedDocumentBlock(
            block_id="b1",
            block_type="paragraph",
            text="Raw original",
            page_number=1,
            source="native_pdf",
            language_metadata=LinguisticMetadata(
                original_text="Raw original",
                cleaned_text="Clean original",
                semantic_role=SemanticRole.UNKNOWN,
                language="en",
                confidence=None,
                processing_provider="deterministic"
            )
        )
        self.assertEqual(block.block_id, "b1")
        self.assertEqual(block.language_metadata.cleaned_text, "Clean original")

if __name__ == "__main__":
    unittest.main()
