import unittest
from services.lesson_planning.guidance.teacher_notes import TeacherNotesGenerator
from services.lesson_planning.guidance.classroom_management import ClassroomManagement
from services.lesson_planning.guidance.misconceptions import Misconceptions
from services.lesson_planning.guidance.materials import MaterialsList
from services.lesson_planning.guidance.preparation import PreparationChecklist
from services.lesson_planning.guidance.reflection import ReflectionPrompts
from services.lesson_planning.guidance.validator import LessonReadinessValidator

class TestTeacherGuidance(unittest.TestCase):
    def test_teacher_notes(self):
        notes = TeacherNotesGenerator.generate("physics")
        self.assertIn("Physics", notes)
        
    def test_classroom_management(self):
        tips = ClassroomManagement.get_tips()
        self.assertEqual(len(tips), 3)
        self.assertIn("Establish clear rules before distributing hands-on STEM materials.", tips)

    def test_misconceptions(self):
        warnings = Misconceptions.get_warnings("chemistry")
        self.assertEqual(len(warnings), 3)
        self.assertIn("Confusing correlation with causation in chemistry analysis.", warnings)

    def test_materials(self):
        materials = MaterialsList.get_materials("math")
        self.assertEqual(len(materials), 3)
        self.assertIn("Worksheets on Math", materials)

    def test_preparation(self):
        steps = PreparationChecklist.get_steps()
        self.assertEqual(len(steps), 3)
        self.assertIn("Verify all computing units are fully charged.", steps)

    def test_reflection(self):
        prompts = ReflectionPrompts.get_prompts()
        self.assertEqual(len(prompts), 3)
        self.assertIn("What concept did students find most challenging?", prompts)

    def test_readiness_perfect_score(self):
        report = LessonReadinessValidator.evaluate_readiness(
            has_objectives=True,
            has_assessment=True,
            is_timing_valid=True,
            has_materials=True
        )
        self.assertEqual(report.readiness_score, 1.0)
        self.assertTrue(report.curriculum_completeness)
        self.assertTrue(report.assessment_completeness)

    def test_readiness_partial_score(self):
        report = LessonReadinessValidator.evaluate_readiness(
            has_objectives=True,
            has_assessment=False,
            is_timing_valid=True,
            has_materials=False
        )
        self.assertEqual(report.readiness_score, 0.50) # 0.30 + 0.20
        self.assertFalse(report.assessment_completeness)
        self.assertTrue(report.timing_validation)

    def test_readiness_zero_score(self):
        report = LessonReadinessValidator.evaluate_readiness(
            has_objectives=False,
            has_assessment=False,
            is_timing_valid=False,
            has_materials=False
        )
        self.assertEqual(report.readiness_score, 0.0)

    def test_readiness_extra_details(self):
        report = LessonReadinessValidator.evaluate_readiness(
            has_objectives=True,
            has_assessment=True,
            is_timing_valid=True,
            has_materials=True,
            extra_details={"notes": "good"}
        )
        self.assertEqual(report.details.get("notes"), "good")

if __name__ == "__main__":
    unittest.main()
