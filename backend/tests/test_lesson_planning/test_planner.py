import unittest
import os
import json
import shutil
import asyncio
from services.lesson_planning.schemas import LessonPlan, LessonSection, LessonTimeline
from services.lesson_planning.config import lpe_config
from services.lesson_planning.factory import ProcessorFactory
from services.lesson_planning.processors.deterministic import DeterministicLessonPlanner
from services.lesson_planning.processors.gemini_processor import GeminiLessonPlanner
from services.lesson_planning.writers.json_writer import JSONWriter
from services.lesson_planning.engine import LessonPlanningEngine

class TestLessonPlanner(unittest.TestCase):
    def setUp(self):
        self.test_job_id = "test_lpe_job"
        self.test_dir = os.path.abspath(os.path.join("uploads/jobs", self.test_job_id))
        os.makedirs(self.test_dir, exist_ok=True)
        
        with open(os.path.join(self.test_dir, "lesson_subject.json"), "w", encoding="utf-8") as f:
            json.dump({"blocks": [{"subject_metadata": {"subject": "physics"}}]}, f)
        with open(os.path.join(self.test_dir, "lesson_subject_graph.json"), "w", encoding="utf-8") as f:
            json.dump({"nodes": [], "edges": []}, f)
        with open(os.path.join(self.test_dir, "lesson_learning_objectives.json"), "w", encoding="utf-8") as f:
            json.dump({"objectives": []}, f)
        with open(os.path.join(self.test_dir, "lesson_instructional_model.json"), "w", encoding="utf-8") as f:
            json.dump({"sequence": [{"concept": "Mechanics", "estimated_minutes": 45, "objectives": ["Apply force."]}]}, f)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_configuration_loading(self):
        self.assertIsNotNone(lpe_config.active_planner_provider)

    def test_factory_selection(self):
        lpe_config.active_planner_provider = "deterministic"
        planner = ProcessorFactory.get_planner()
        self.assertIsInstance(planner, DeterministicLessonPlanner)
        
        lpe_config.active_planner_provider = "gemini"
        planner_gem = ProcessorFactory.get_planner()
        self.assertIsInstance(planner_gem, GeminiLessonPlanner)

    def test_schema_validation(self):
        section = LessonSection(title="Introduction", duration_minutes=30, description="Overview.")
        self.assertEqual(section.duration_minutes, 30)
        
        from services.lesson_planning.schemas import ValidationReport
        report = ValidationReport(valid=True, total_duration_minutes=30)
        
        plan = LessonPlan(
            generated_at="2026-07-12T00:00:00",
            subject="physics",
            title="Newton's Laws",
            lesson_structure="Base structure",
            lesson_sections=[section],
            timeline=["Introduction"],
            validation_report=report
        )
        self.assertEqual(plan.subject, "physics")

    def test_deterministic_planner(self):
        planner = DeterministicLessonPlanner()
        context = {
            "instructional_model": {"sequence": [{"concept": "Force", "estimated_minutes": 45, "objectives": ["Analyze F=ma"]}]},
            "subject": {"output_file": "path_subject"},
            "graph": {"output_file": "path_graph"},
            "objectives": {"output_file": "path_obj"},
            "instructional_model": {"output_file": "path_inst", "sequence": [{"concept": "Force", "estimated_minutes": 45, "objectives": ["Analyze F=ma"]}]}
        }
        plan = asyncio.run(planner.plan("physics", context))
        self.assertEqual(len(plan.lesson_sections), 10)
        self.assertEqual(plan.lesson_sections[0].title, "Introduction")

    def test_engine_process_and_writer(self):
        lpe_config.active_planner_provider = "deterministic"
        engine = LessonPlanningEngine(self.test_job_id)
        
        output_file = asyncio.run(engine.process())
        
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r", encoding="utf-8") as f:
            plan_data = json.load(f)
            self.assertEqual(plan_data["engine_name"], "Lesson Planning Engine")
            self.assertEqual(plan_data["subject"], "physics")
            self.assertEqual(len(plan_data["lesson_sections"]), 10)
            self.assertEqual(plan_data["lesson_sections"][0]["title"], "Introduction")

if __name__ == "__main__":
    unittest.main()
