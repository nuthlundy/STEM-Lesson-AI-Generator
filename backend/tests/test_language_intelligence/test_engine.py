import unittest
import asyncio
import os
import shutil
import json
from services.language_intelligence.engine import LanguageIntelligenceEngine
from services.document_intelligence.interfaces import (
    DocumentIntelligenceResult,
    DocumentMetadata,
    DocumentBlock,
    ProcessingMetrics
)

class TestLanguageIntelligenceEngine(unittest.TestCase):
    def setUp(self):
        self.test_base_dir = os.path.abspath("backend/tests/temp_jobs_lie")
        self.job_id = "test-job-lie"
        self.job_dir = os.path.join(self.test_base_dir, self.job_id)
        os.makedirs(self.job_dir, exist_ok=True)
        
        # Create mock lesson.json
        meta = DocumentMetadata(
            job_id=self.job_id,
            original_filename="test.pdf",
            total_pages=1,
            processing_time_sec=1.0,
            requires_ocr=False
        )
        block = DocumentBlock(
            block_id="b1",
            block_type="paragraph",
            text="This is an  exmaple.",
            page_number=1,
            source="native_pdf"
        )
        res = DocumentIntelligenceResult(metadata=meta, blocks=[block])
        
        with open(os.path.join(self.job_dir, "lesson.json"), "w", encoding="utf-8") as f:
            f.write(res.model_dump_json())

    def tearDown(self):
        if os.path.exists(self.test_base_dir):
            shutil.rmtree(self.test_base_dir)

    def test_engine_processing(self):
        # Force deterministic fallback so test runs reliably without API keys
        import sys
        from unittest.mock import MagicMock
        sys.modules['google.generativeai'] = MagicMock()
        
        engine = LanguageIntelligenceEngine(job_id=self.job_id, base_dir=self.test_base_dir)
        # Ensure it's not configured to use the fake genai mock
        engine.processor.is_configured = False 
        
        output_file = asyncio.run(engine.process())
        
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.assertEqual(len(data["blocks"]), 1)
        self.assertIn("language_metadata", data["blocks"][0])
        self.assertEqual(data["blocks"][0]["language_metadata"]["cleaned_text"], "This is an exmaple.")

if __name__ == "__main__":
    unittest.main()
