import unittest
import os
import json
from services.subject_intelligence.curriculum.bloom import BloomTaxonomyClassifier
from services.subject_intelligence.curriculum.validator import ObjectiveValidator
from services.subject_intelligence.curriculum.standards import StandardsAlignmentEngine
from services.subject_intelligence.constants import STEMSubject

class TestCurriculumAlignment(unittest.TestCase):
    def test_bloom_classifier(self):
        self.assertEqual(BloomTaxonomyClassifier.classify("Define what mass means."), "Remember")
        self.assertEqual(BloomTaxonomyClassifier.classify("Calculate the derivative of x^2."), "Apply")
        self.assertEqual(BloomTaxonomyClassifier.classify("Design an algorithm to sort arrays."), "Create")
        self.assertEqual(BloomTaxonomyClassifier.classify("Vague description without verbs."), "Understand") # fallback

    def test_objective_validator(self):
        # Valid objective
        report1 = ObjectiveValidator.validate("Explain the second law of motion clearly.")
        self.assertTrue(report1["valid"])
        self.assertEqual(len(report1["errors"]), 0)

        # Invalid: Too short
        report2 = ObjectiveValidator.validate("Calculate force.")
        self.assertFalse(report2["valid"])
        self.assertIn("Objective is too short to be specific (minimum 5 words required).", report2["errors"])

        # Invalid: Vague verb
        report3 = ObjectiveValidator.validate("Learn about atomic chemical bonds today.")
        self.assertFalse(report3["valid"])
        self.assertIn("Objective uses a vague/non-measurable verb 'learn'. Use action verbs instead.", report3["errors"])

    def test_standards_alignment(self):
        # Physics match
        aligns1 = StandardsAlignmentEngine.get_alignments(STEMSubject.PHYSICS, ["Mechanics", "force"])
        self.assertEqual(len(aligns1), 1)
        self.assertEqual(aligns1[0].standard_code, "NGSS.HS-PS2-1")
        self.assertIn("Mechanics", aligns1[0].aligned_concepts)

        # CS match
        aligns2 = StandardsAlignmentEngine.get_alignments(STEMSubject.COMPUTER_SCIENCE, ["recursion", "sorting"])
        self.assertEqual(len(aligns2), 1)
        self.assertEqual(aligns2[0].standard_code, "CSTA.3A-AP-17")

if __name__ == "__main__":
    unittest.main()
