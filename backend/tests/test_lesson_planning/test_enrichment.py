import sys
import unittest
import json
import asyncio
from unittest.mock import MagicMock, patch

# Mock google.generativeai module
sys.modules['google.generativeai'] = MagicMock()

from services.lesson_planning.schemas import LessonPlan, LessonSection, ValidationReport
from services.lesson_planning.utils.cache import LessonCache
from services.lesson_planning.processors.merge_engine import AIMergeEngine
from services.lesson_planning.processors.gemini_processor import GeminiLessonPlanner
from services.lesson_planning.config import lpe_config

class TestAIEnrichment(unittest.TestCase):
    def test_cache_set_and_get(self):
        cache = LessonCache()
        cache.clear()
        
        self.assertIsNone(cache.get("non_existent"))
        
        data = {"confidence": 0.95, "notes": "some notes"}
        cache.set("query_text", data)
        self.assertEqual(cache.get("query_text"), data)
        
        cache.clear()
        self.assertIsNone(cache.get("query_text"))

    def test_ai_merge_engine_primacy(self):
        # Deterministic source
        report = ValidationReport(valid=True, total_duration_minutes=60)
        det_plan = LessonPlan(
            generated_at="2026-07-12T00:00:00",
            subject="chemistry",
            title="Periodic Table",
            lesson_structure="Det Structure",
            lesson_sections=[
                LessonSection(title="Introduction", duration_minutes=10, description="Overview.")
            ],
            timeline=["Introduction"],
            validation_report=report
        )
        
        ai_data = {
            "teacher_notes": {"Introduction": "Rich context about atoms."},
            "engagement_suggestions": {"Introduction": "Show a real element."},
            "pacing_recommendations": {"Introduction": "10 minutes sharp."},
            "confidence": 0.98
        }
        
        merged = AIMergeEngine.merge(det_plan, ai_data)
        
        # Invariants preserved
        self.assertEqual(merged.subject, "chemistry")
        self.assertEqual(merged.title, "Periodic Table")
        self.assertEqual(merged.lesson_sections[0].title, "Introduction")
        
        # Enriched fields loaded
        self.assertEqual(merged.teacher_notes["Introduction"], "Rich context about atoms.")
        self.assertEqual(merged.engagement_suggestions["Introduction"], "Show a real element.")
        self.assertEqual(merged.confidence, 0.98)

    def test_gemini_planner_no_key_fallback(self):
        # Force config state
        lpe_config.gemini_api_key = ""
        planner = GeminiLessonPlanner()
        
        context = {
            "instructional_model": {"sequence": []},
            "subject": {"output_file": "path_subject"},
            "graph": {"output_file": "path_graph"},
            "objectives": {"output_file": "path_obj"},
            "instructional_model": {"output_file": "path_inst"}
        }
        
        plan = asyncio.run(planner.plan("chemistry", context))
        self.assertIsNone(plan.ai_enrichment)
        self.assertEqual(plan.confidence, None)

    @patch("services.lesson_planning.processors.gemini_processor.HAS_GENAI", True)
    @patch("services.lesson_planning.processors.gemini_processor.genai")
    def test_gemini_planner_with_key_api_call(self, mock_genai):
        lpe_config.gemini_api_key = "fake_key"
        planner = GeminiLessonPlanner()
        
        # Mock API response
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "teacher_notes": {"Introduction": "AI notes"},
            "engagement_suggestions": {"Introduction": "AI engagement"},
            "pacing_recommendations": {"Introduction": "AI pacing"},
            "enhanced_transitions": {},
            "confidence": 0.92
        })
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        context = {
            "instructional_model": {"sequence": []},
            "subject": {"output_file": "path_subject"},
            "graph": {"output_file": "path_graph"},
            "objectives": {"output_file": "path_obj"},
            "instructional_model": {"output_file": "path_inst"}
        }
        
        plan = asyncio.run(planner.plan("chemistry", context))
        self.assertIsNotNone(plan.ai_enrichment)
        self.assertEqual(plan.confidence, 0.92)
        self.assertEqual(plan.teacher_notes["Introduction"], "AI notes")

    def test_cache_clear(self):
        cache = LessonCache()
        cache.set("key", {"val": 1})
        cache.clear()
        self.assertIsNone(cache.get("key"))

    def test_merge_missing_keys(self):
        report = ValidationReport(valid=True, total_duration_minutes=60)
        det_plan = LessonPlan(
            generated_at="2026-07-12T00:00:00",
            subject="chemistry",
            title="Periodic Table",
            lesson_structure="Det Structure",
            lesson_sections=[
                LessonSection(title="Introduction", duration_minutes=10, description="Overview.")
            ],
            timeline=["Introduction"],
            validation_report=report
        )
        ai_data = {} # completely empty AI data
        merged = AIMergeEngine.merge(det_plan, ai_data)
        self.assertEqual(merged.teacher_notes["Introduction"], "Default notes for Introduction.")
        self.assertEqual(merged.confidence, 0.90)

    @patch("services.lesson_planning.processors.gemini_processor.HAS_GENAI", True)
    @patch("services.lesson_planning.processors.gemini_processor.genai")
    def test_gemini_planner_cache_hit(self, mock_genai):
        lpe_config.gemini_api_key = "fake_key"
        planner = GeminiLessonPlanner()
        planner._cache.clear()
        
        # Manually seed cache
        cache_key = "chemistry:['Introduction', 'Learning Objectives', 'Prior Knowledge', 'Lesson Development', 'Guided Practice', 'Independent Practice', 'Review', 'Reflection', 'Homework Placeholder', 'Closing']"
        planner._cache.set(cache_key, {
            "teacher_notes": {"Introduction": "Cached notes"},
            "confidence": 0.99
        })
        
        context = {
            "instructional_model": {"sequence": []},
            "subject": {"output_file": "path_subject"},
            "graph": {"output_file": "path_graph"},
            "objectives": {"output_file": "path_obj"},
            "instructional_model": {"output_file": "path_inst"}
        }
        
        plan = asyncio.run(planner.plan("chemistry", context))
        self.assertEqual(plan.teacher_notes["Introduction"], "Cached notes")
        self.assertEqual(plan.confidence, 0.99)
        mock_genai.GenerativeModel.assert_not_called()

    @patch("services.lesson_planning.processors.gemini_processor.HAS_GENAI", True)
    @patch("services.lesson_planning.processors.gemini_processor.genai")
    def test_gemini_planner_exception_fallback(self, mock_genai):
        lpe_config.gemini_api_key = "fake_key"
        planner = GeminiLessonPlanner()
        planner._cache.clear()
        
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API offline")
        mock_genai.GenerativeModel.return_value = mock_model
        
        context = {
            "instructional_model": {"sequence": []},
            "subject": {"output_file": "path_subject"},
            "graph": {"output_file": "path_graph"},
            "objectives": {"output_file": "path_obj"},
            "instructional_model": {"output_file": "path_inst"}
        }
        
        plan = asyncio.run(planner.plan("chemistry", context))
        self.assertIsNone(plan.ai_enrichment)
        self.assertIsNone(plan.confidence)

    def test_prompt_content(self):
        from services.lesson_planning.prompts.repository import LESSON_ENRICHMENT_PROMPT
        self.assertIn("{subject}", LESSON_ENRICHMENT_PROMPT)
        self.assertIn("{sections}", LESSON_ENRICHMENT_PROMPT)
        self.assertIn("{objectives}", LESSON_ENRICHMENT_PROMPT)

if __name__ == "__main__":
    unittest.main()
