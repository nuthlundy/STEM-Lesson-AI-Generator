import unittest
from services.document_intelligence.interfaces import (
    BoundingBox,
    ExtractedAsset,
    DocumentBlock,
    ProcessingMetrics,
    DocumentMetadata,
    DocumentIntelligenceResult
)

class TestInterfaces(unittest.TestCase):
    def test_bounding_box(self):
        bbox = BoundingBox(x0=0.0, y0=0.0, x1=100.0, y1=100.0)
        self.assertEqual(bbox.x0, 0.0)
        self.assertEqual(bbox.y1, 100.0)

    def test_extracted_asset(self):
        asset = ExtractedAsset(
            asset_id="asset_1",
            asset_type="image",
            page_number=1,
            confidence=0.95,
            source="image",
            file_path="uploads/jobs/123/assets/img.png"
        )
        self.assertEqual(asset.asset_id, "asset_1")
        self.assertEqual(asset.confidence, 0.95)
        self.assertEqual(asset.source, "image")

    def test_extracted_asset_invalid_confidence(self):
        with self.assertRaises(ValueError):
            ExtractedAsset(
                asset_id="asset_1",
                asset_type="image",
                page_number=1,
                confidence=1.5,  # Exceeds max 1.0
                source="image"
            )

    def test_document_block(self):
        block = DocumentBlock(
            block_id="block_1",
            block_type="paragraph",
            text="Hello world",
            page_number=1,
            confidence=0.88,
            source="native_pdf"
        )
        self.assertEqual(block.block_id, "block_1")
        self.assertEqual(block.confidence, 0.88)
        self.assertEqual(block.source, "native_pdf")

    def test_document_metadata_schema_version(self):
        metadata = DocumentMetadata(
            job_id="job_123",
            original_filename="test.pdf",
            total_pages=5,
            processing_time_sec=1.5,
            requires_ocr=False
        )
        self.assertEqual(metadata.schema_version, "1.0.0")

if __name__ == "__main__":
    unittest.main()
