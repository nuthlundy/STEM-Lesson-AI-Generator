import unittest
import asyncio
import os
import shutil
import json
from services.subject_intelligence.engine import SubjectIntelligenceEngine
from services.language_intelligence.interfaces import (
    LanguageIntelligenceResult,
    EnrichedDocumentBlock,
    LinguisticMetadata,
    SemanticRole
)
from services.document_intelligence.interfaces import DocumentMetadata

class TestSubjectIntelligenceEngine(unittest.TestCase):
    def setUp(self):
        self.test_base_dir = os.path.abspath("backend/tests/temp_jobs_sie")
        self.job_id = "test-job-sie"
        self.job_dir = os.path.join(self.test_base_dir, self.job_id)
        os.makedirs(self.job_dir, exist_ok=True)
        
        # Create a mock lesson_language.json
        meta = DocumentMetadata(
            job_id=self.job_id,
            original_filename="test.pdf",
            total_pages=1,
            processing_time_sec=1.0,
            requires_ocr=False
        )
        ling_meta = LinguisticMetadata(
            original_text="F = ma",
            cleaned_text="F = ma",
            semantic_role=SemanticRole.UNKNOWN,
            keywords=[],
            language="en",
            confidence=None,
            processing_provider="deterministic",
            model_version=None
        )
        block = EnrichedDocumentBlock(
            block_id="b1",
            block_type="equation",
            text="F = ma",
            page_number=1,
            source="equation",
            language_metadata=ling_meta
        )
        res = LanguageIntelligenceResult(metadata=meta, blocks=[block])
        
        with open(os.path.join(self.job_dir, "lesson_language.json"), "w", encoding="utf-8") as f:
            f.write(res.model_dump_json())

    def tearDown(self):
        if os.path.exists(self.test_base_dir):
            shutil.rmtree(self.test_base_dir)

    def test_engine_processing_and_metadata(self):
        hook_calls = []
        
        class HookedEngine(SubjectIntelligenceEngine):
            def before_process(self, input_data):
                super().before_process(input_data)
                hook_calls.append("before_process")
                
            def after_process(self, blocks):
                super().after_process(blocks)
                hook_calls.append("after_process")
                
            def before_validate(self, blocks):
                super().before_validate(blocks)
                hook_calls.append("before_validate")
                
            def after_validate(self, val):
                super().after_validate(val)
                hook_calls.append("after_validate")
                
            def before_save(self, res):
                super().before_save(res)
                hook_calls.append("before_save")
                
            def after_save(self):
                super().after_save()
                hook_calls.append("after_save")
                
        engine = HookedEngine(job_id=self.job_id, base_dir=self.test_base_dir)
        engine.processor.is_configured = False # Force deterministic
        
        output_file = asyncio.run(engine.process())
        
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.exists(os.path.join(self.job_dir, "lesson_subject_graph.json")))
        self.assertTrue(os.path.exists(os.path.join(self.job_dir, "lesson_learning_objectives.json")))
        self.assertTrue(os.path.exists(os.path.join(self.job_dir, "lesson_instructional_model.json")))
        
        # Verify metadata
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.assertEqual(data["engine_name"], "Subject Intelligence Engine")
        self.assertEqual(data["engine_version"], "1.0.0")
        self.assertEqual(data["schema_version"], "1.0.0")
        
        # Verify hooks sequence
        self.assertEqual(
            hook_calls,
            [
                "before_process",
                "after_process",
                "before_validate",
                "after_validate",
                "before_save",
                "after_save"
            ]
        )

if __name__ == "__main__":
    unittest.main()
