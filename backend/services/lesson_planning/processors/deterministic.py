import datetime
from typing import Dict, Any
from services.lesson_planning.interfaces.planner import LessonPlanner
from services.lesson_planning.schemas import LessonPlan, LessonSection, LessonTimeline
from services.lesson_planning.processors.sequencer import LessonSectionSequencer
from services.lesson_planning.processors.allocator import TimeAllocationEngine
from services.lesson_planning.processors.mapper import ObjectiveMapper
from services.lesson_planning.processors.transitions import TransitionGenerator
from services.lesson_planning.processors.validator import TimelineValidator

class DeterministicLessonPlanner(LessonPlanner):
    """Generates standard default lesson plan sequences deterministically based on context."""
    async def plan(self, subject: str, context_data: Dict[str, Any]) -> LessonPlan:
        # 1. Total duration estimation
        inst_model = context_data.get("instructional_model", {})
        sequence_steps = inst_model.get("sequence", [])
        total_duration = sum(step.get("estimated_minutes", 45) for step in sequence_steps)
        if total_duration <= 0:
            total_duration = 80 # Default standard duration
            
        # 2. Get ordered sections
        ordered_titles = LessonSectionSequencer.get_sequence()
        
        # 3. Allocate time
        durations = TimeAllocationEngine.allocate_durations(total_duration)
        
        # 4. Map objectives
        objectives_list = context_data.get("objectives", {}).get("objectives", [])
        obj_mapping = ObjectiveMapper.map_objectives(objectives_list)
        
        # 5. Generate transitions
        transitions = TransitionGenerator.generate_transitions(ordered_titles)
        
        # 6. Build sections list
        lesson_sections = []
        for title in ordered_titles:
            sec_duration = durations.get(title, 5)
            
            # Map descriptions and objectives matching this section title
            mapped_objectives = []
            for obj in objectives_list:
                obj_id = obj.get("id")
                if obj_id in obj_mapping and title in obj_mapping[obj_id]:
                    mapped_objectives.append(obj.get("description", ""))
                    
            lesson_sections.append(LessonSection(
                title=title,
                duration_minutes=sec_duration,
                objectives=mapped_objectives,
                description=f"Deterministic instructional walkthrough for {title} segment."
            ))
            
        # 7. Validate timeline
        validation_report = TimelineValidator.validate(
            sections=lesson_sections,
            timeline=ordered_titles,
            objective_mapping=obj_mapping,
            expected_objectives_count=len(objectives_list)
        )
        
        # 8. Generate differentiation block
        from services.lesson_planning.differentiation.generator import DifferentiationGenerator
        diff_block = DifferentiationGenerator.generate_default()
        
        # 9. Generate assessment plan
        from services.lesson_planning.assessment.planner import AssessmentPlanner
        assessment_block = AssessmentPlanner.plan_assessment(subject, objectives_list, lesson_sections)
        
        # 10. Generate teacher guidance and readiness
        from services.lesson_planning.guidance.teacher_notes import TeacherNotesGenerator
        from services.lesson_planning.guidance.classroom_management import ClassroomManagement
        from services.lesson_planning.guidance.misconceptions import Misconceptions
        from services.lesson_planning.guidance.materials import MaterialsList
        from services.lesson_planning.guidance.preparation import PreparationChecklist
        from services.lesson_planning.guidance.reflection import ReflectionPrompts
        from services.lesson_planning.guidance.validator import LessonReadinessValidator
        
        guidance_notes = TeacherNotesGenerator.generate(subject)
        management_tips = ClassroomManagement.get_tips()
        warnings = Misconceptions.get_warnings(subject)
        materials_needed = MaterialsList.get_materials(subject)
        prep_steps = PreparationChecklist.get_steps()
        self_reflection = ReflectionPrompts.get_prompts()
        
        has_objectives = len(objectives_list) > 0
        has_assessment = len(assessment_block.assessment_blueprint) > 0
        is_timing_valid = validation_report.valid
        has_materials = len(materials_needed) > 0
        
        readiness_report = LessonReadinessValidator.evaluate_readiness(
            has_objectives=has_objectives,
            has_assessment=has_assessment,
            is_timing_valid=is_timing_valid,
            has_materials=has_materials,
            extra_details={
                "validation_errors": validation_report.errors,
                "sections_count": len(lesson_sections)
            }
        )
        
        return LessonPlan(
            generated_at=datetime.datetime.now().isoformat(),
            source_artifacts={
                "subject": context_data.get("subject", {}).get("output_file"),
                "graph": context_data.get("graph", {}).get("output_file"),
                "objectives": context_data.get("objectives", {}).get("output_file"),
                "instructional_model": context_data.get("instructional_model", {}).get("output_file")
            },
            subject=subject,
            title=f"Lesson Plan: {subject.capitalize()}",
            lesson_structure="Standard 10-part deterministic lesson timeline plan.",
            lesson_sections=lesson_sections,
            timeline=ordered_titles,
            transitions=transitions,
            objective_mapping=obj_mapping,
            validation_report=validation_report,
            
            # Differentiation fields
            differentiation=diff_block,
            learner_profiles=diff_block.learner_profiles,
            accommodations=diff_block.accommodations,
            intervention_strategies=diff_block.intervention_strategies,
            enrichment_recommendations=diff_block.enrichment_recommendations,
            
            # Assessment fields
            assessment_plan=assessment_block,
            assessment_blueprint=assessment_block.assessment_blueprint,
            bloom_distribution=assessment_block.bloom_distribution,
            question_distribution=assessment_block.question_distribution,
            assessment_alignment=assessment_block.assessment_alignment,
            
            # Guidance fields
            teacher_guidance=guidance_notes,
            materials=materials_needed,
            preparation=prep_steps,
            classroom_management=management_tips,
            misconceptions=warnings,
            reflection_prompts=self_reflection,
            lesson_readiness=readiness_report
        )
