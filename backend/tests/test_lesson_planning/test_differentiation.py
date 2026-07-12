import unittest
from services.lesson_planning.differentiation.profiles import LearnerProfiles
from services.lesson_planning.differentiation.strategies import DifferentiationStrategies
from services.lesson_planning.differentiation.accommodations import Accommodations
from services.lesson_planning.differentiation.enrichment import Enrichment
from services.lesson_planning.differentiation.intervention import Intervention
from services.lesson_planning.differentiation.generator import DifferentiationGenerator

class TestDifferentiation(unittest.TestCase):
    def test_profiles_list(self):
        profiles = LearnerProfiles.get_all_profiles()
        self.assertEqual(len(profiles), 6)
        self.assertIn("English Language Learners (ELL)", profiles)

    def test_profiles_consts(self):
        self.assertEqual(LearnerProfiles.GIFTED, "Gifted Learners")

    def test_strategies_content(self):
        strategies = DifferentiationStrategies.get_default_strategies()
        self.assertEqual(len(strategies), 6)
        self.assertIn("Gifted Learners", strategies)

    def test_accommodations_content(self):
        accommodations = Accommodations.get_default_accommodations()
        self.assertEqual(len(accommodations), 6)
        self.assertIn("English Language Learners (ELL)", accommodations)

    def test_enrichment_content(self):
        enrichment = Enrichment.get_default_enrichment()
        self.assertEqual(len(enrichment), 6)
        self.assertIn("Below Grade Level", enrichment)

    def test_intervention_content(self):
        intervention = Intervention.get_default_intervention()
        self.assertEqual(len(intervention), 6)
        self.assertIn("Students with Special Educational Needs (SEN)", intervention)

    def test_generator_default_block(self):
        block = DifferentiationGenerator.generate_default()
        self.assertEqual(len(block.learner_profiles), 6)
        self.assertEqual(len(block.accommodations), 6)
        self.assertEqual(len(block.intervention_strategies), 6)
        self.assertEqual(len(block.enrichment_recommendations), 6)

    def test_generator_exact_mappings(self):
        block = DifferentiationGenerator.generate_default()
        self.assertIn("Provide printed templates and mathematical reference sheets.", block.accommodations[LearnerProfiles.BELOW_GRADE])

    def test_profiles_contains_ell(self):
        self.assertTrue(any("ELL" in p for p in LearnerProfiles.get_all_profiles()))
        
    def test_profiles_contains_sen(self):
        self.assertTrue(any("SEN" in p for p in LearnerProfiles.get_all_profiles()))

if __name__ == "__main__":
    unittest.main()
