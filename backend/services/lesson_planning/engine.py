import os
import json
from typing import Dict, Any, Optional, Callable
from services.lesson_planning.factory import ProcessorFactory
from services.lesson_planning.writers.json_writer import JSONWriter
from services.lesson_planning.schemas import LessonPlan
from core.logger import get_logger

class LessonPlanningEngine:
    def __init__(self, job_id: str, base_dir: str = "uploads/jobs"):
        self.job_id = job_id
        self.base_dir = base_dir
        self.job_dir = os.path.abspath(os.path.join(self.base_dir, self.job_id))
        
        # Input files
        self.subject_file = os.path.join(self.job_dir, "lesson_subject.json")
        self.graph_file = os.path.join(self.job_dir, "lesson_subject_graph.json")
        self.objectives_file = os.path.join(self.job_dir, "lesson_learning_objectives.json")
        self.instructional_file = os.path.join(self.job_dir, "lesson_instructional_model.json")
        
        # Output file
        self.output_file = os.path.join(self.job_dir, "lesson_plan.json")
        
        self.logger = get_logger("stem_ai.lpe.engine")
        self.planner = ProcessorFactory.get_planner()
        self.writer = JSONWriter()

    # Lifecycle Hooks Skeletons
    def before_plan(self, context_data: Dict[str, Any]) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: before_plan")

    def after_plan(self, plan: LessonPlan) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: after_plan. Created title: {plan.title}")

    def before_save(self, plan: LessonPlan) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: before_save")

    def after_save(self) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: after_save. Saved output to {self.output_file}")

    async def process(self, progress_callback: Optional[Callable[[int, str], None]] = None) -> str:
        """
        Orchestrates lesson planning based on subject intelligence files.
        Returns the absolute filepath to lesson_plan.json.
        """
        if progress_callback:
            progress_callback(0, "Initializing Lesson Planning Engine.")
            
        files_to_check = {
            "subject": self.subject_file,
            "graph": self.graph_file,
            "objectives": self.objectives_file,
            "instructional_model": self.instructional_file
        }
        
        context_data = {}
        for key, filepath in files_to_check.items():
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Required input file missing: {filepath}")
            with open(filepath, "r", encoding="utf-8") as f:
                context_data[key] = json.load(f)
                context_data[key]["output_file"] = filepath

        # Hook: before_plan
        self.before_plan(context_data)
        
        if progress_callback:
            progress_callback(30, "Context files loaded. Starting planner.")

        subject_info = context_data["subject"]
        blocks = subject_info.get("blocks", [])
        dominant_subject = "math"
        if blocks:
            first_block = blocks[0]
            if "subject_metadata" in first_block and first_block["subject_metadata"]:
                dominant_subject = first_block["subject_metadata"].get("subject", "math")

        lesson_plan = await self.planner.plan(dominant_subject, context_data)

        # Hook: after_plan
        self.after_plan(lesson_plan)

        if progress_callback:
            progress_callback(80, "Planning complete. Writing lesson_plan.json.")

        # Hook: before_save
        self.before_save(lesson_plan)

        # Write output asynchronously
        await self.writer.write(lesson_plan, self.output_file)

        # Hook: after_save
        self.after_save()

        if progress_callback:
            progress_callback(100, "Lesson Planning Engine complete.")

        return self.output_file
