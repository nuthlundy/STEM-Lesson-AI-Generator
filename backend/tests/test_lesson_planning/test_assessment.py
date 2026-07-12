import unittest
from services.lesson_planning.schemas import AssessmentPlan, AssessmentBlueprintItem, AssessmentAlignment, LessonSection
from services.lesson_planning.assessment.taxonomy import BloomTaxonomy
from services.lesson_planning.assessment.weighting import AssessmentWeighting
from services.lesson_planning.assessment.blueprint import AssessmentBlueprintBuilder
from services.lesson_planning.assessment.validator import AssessmentValidator
from services.lesson_planning.assessment.planner import AssessmentPlanner

class TestAssessmentPlanning(unittest.TestCase):
    def test_bloom_levels(self):
        levels = BloomTaxonomy.get_levels()
        self.assertEqual(len(levels), 6)
        self.assertIn("Applying", levels)
        
    def test_bloom_distribution(self):
        alignments = [
            AssessmentAlignment(
                assessment_objective="Obj1",
                lesson_objective_id="L1",
                bloom_level="Applying",
                curriculum_standard="CCSS",
                lesson_section="Intro",
                concept="gravity"
            ),
            AssessmentAlignment(
                assessment_objective="Obj2",
                lesson_objective_id="L2",
                bloom_level="Understanding",
                curriculum_standard="CCSS",
                lesson_section="Intro",
                concept="gravity"
            )
        ]
        dist = BloomTaxonomy.calculate_distribution(alignments)
        self.assertEqual(dist["Applying"], 0.5)
        self.assertEqual(dist["Understanding"], 0.5)
        self.assertEqual(dist["Remembering"], 0.0)

    def test_bloom_distribution_empty(self):
        dist = BloomTaxonomy.calculate_distribution([])
        self.assertEqual(dist["Applying"], 0.0)

    def test_weighting_question_distribution(self):
        blueprint = [
            AssessmentBlueprintItem(
                assessment_type="Exit Ticket",
                topic="Exit Check",
                weight=0.1,
                target_questions_count=3
            ),
            AssessmentBlueprintItem(
                assessment_type="Formative",
                topic="Mid-Lesson Check",
                weight=0.3,
                target_questions_count=5
            )
        ]
        dist = AssessmentWeighting.calculate_question_distribution(blueprint)
        self.assertEqual(dist["Exit Ticket"], 3)
        self.assertEqual(dist["Formative"], 5)

    def test_blueprint_builder_default(self):
        objs = [{"id": "obj_1", "description": "Learn math", "bloom_level": "Applying", "concept": "math"}]
        sections = [LessonSection(title="Introduction", duration_minutes=10, description="Intro")]
        bp = AssessmentBlueprintBuilder.build_default("math", objs, sections)
        self.assertEqual(len(bp), 3) # Exit, Formative, Summative
        self.assertEqual(bp[0].assessment_type, "Exit Ticket")
        self.assertEqual(bp[0].alignment[0].lesson_section, "Introduction")

    def test_validator_valid_plan(self):
        plan = AssessmentPlan(
            assessment_blueprint=[],
            bloom_distribution={},
            question_distribution={},
            assessment_alignment=[
                AssessmentAlignment(
                    assessment_objective="Obj",
                    lesson_objective_id="L1",
                    bloom_level="Applying",
                    curriculum_standard="CCSS",
                    lesson_section="Intro",
                    concept="gravity"
                )
            ]
        )
        self.assertTrue(AssessmentValidator.validate(plan))

    def test_validator_invalid_plan(self):
        plan = AssessmentPlan(
            assessment_blueprint=[],
            bloom_distribution={},
            question_distribution={},
            assessment_alignment=[
                AssessmentAlignment(
                    assessment_objective="Obj",
                    lesson_objective_id="L1",
                    bloom_level="InvalidLevel", # Invalid Bloom level
                    curriculum_standard="CCSS",
                    lesson_section="Intro",
                    concept="gravity"
                )
            ]
        )
        self.assertFalse(AssessmentValidator.validate(plan))

    def test_validator_empty_plan(self):
        plan = AssessmentPlan(
            assessment_blueprint=[],
            bloom_distribution={},
            question_distribution={},
            assessment_alignment=[]
        )
        self.assertFalse(AssessmentValidator.validate(plan))

    def test_planner_orchestrates(self):
        objs = [{"id": "obj_1", "description": "Learn math", "bloom_level": "Applying", "concept": "math"}]
        sections = [LessonSection(title="Introduction", duration_minutes=10, description="Intro")]
        plan = AssessmentPlanner.plan_assessment("math", objs, sections)
        self.assertEqual(len(plan.assessment_blueprint), 3)
        self.assertIn("Applying", plan.bloom_distribution)

    def test_blueprint_empty_objectives_fallback(self):
        bp = AssessmentBlueprintBuilder.build_default("math", [], [])
        self.assertEqual(len(bp), 3)
        self.assertEqual(bp[0].alignment[0].lesson_objective_id, "OBJ-01")

if __name__ == "__main__":
    unittest.main()
