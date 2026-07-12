from typing import List, Dict, Any
from services.lesson_planning.schemas import ValidationReport, LessonSection

class TimelineValidator:
    """Verifies that the generated lesson timeline satisfies ordering, duration, and mapping invariants."""
    
    @staticmethod
    def validate(
        sections: List[LessonSection],
        timeline: List[str],
        objective_mapping: Dict[str, List[str]],
        expected_objectives_count: int
    ) -> ValidationReport:
        errors = []
        warnings = []
        
        total_duration = sum(s.duration_minutes for s in sections)
        if total_duration < 30 or total_duration > 180:
            errors.append(f"Total duration ({total_duration} mins) must be between 30 and 180 minutes.")
            
        from services.lesson_planning.processors.sequencer import LessonSectionSequencer
        expected_order = LessonSectionSequencer.get_sequence()
        
        actual_order = [s.title for s in sections]
        if actual_order != expected_order:
            errors.append(f"Lesson sections ordering mismatch. Expected: {expected_order}, got: {actual_order}")
            
        if len(objective_mapping) < expected_objectives_count:
            warnings.append(f"Some objectives might not be mapped. Mapped: {len(objective_mapping)} / Expected: {expected_objectives_count}")
            
        for obj_id, secs in objective_mapping.items():
            if not secs:
                errors.append(f"Objective '{obj_id}' is mapped to no sections.")
                
        return ValidationReport(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            total_duration_minutes=total_duration
        )
