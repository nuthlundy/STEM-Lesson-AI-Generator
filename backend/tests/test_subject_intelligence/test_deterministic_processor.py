import unittest
import asyncio
from services.subject_intelligence.processors.deterministic import DeterministicSubjectProcessor
from services.subject_intelligence.constants import STEMSubject

class TestDeterministicSubjectProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DeterministicSubjectProcessor()

    def test_math_detection(self):
        text = "This theorem describes a matrix function and the derivative equation."
        result = asyncio.run(self.processor.process(text))
        
        self.assertEqual(result.subject, STEMSubject.MATH)
        self.assertEqual(result.topic, "Calculus")
        self.assertIn("matrix", result.vocabulary)
        self.assertIn("derivative", result.vocabulary)
        self.assertEqual(result.difficulty, "medium")

    def test_physics_detection_and_relationships(self):
        text = "The force of gravity depends on mass and velocity in quantum mechanics."
        result = asyncio.run(self.processor.process(text))
        
        self.assertEqual(result.subject, STEMSubject.PHYSICS)
        self.assertEqual(result.topic, "Mechanics")
        self.assertIn("gravity", result.vocabulary)
        self.assertIn("force", result.vocabulary)
        self.assertIn("classical mechanics", result.prerequisites)

    def test_chemistry_detection(self):
        text = "An organic molecule forms a covalent bond during this reaction."
        result = asyncio.run(self.processor.process(text))
        
        self.assertEqual(result.subject, STEMSubject.CHEMISTRY)
        self.assertEqual(result.topic, "Organic Chemistry")
        self.assertIn("molecule", result.vocabulary)

    def test_cs_detection(self):
        text = "A binary search algorithm uses recursion to traverse an array."
        result = asyncio.run(self.processor.process(text))
        
        self.assertEqual(result.subject, STEMSubject.COMPUTER_SCIENCE)
        self.assertEqual(result.topic, "Algorithms & Data Structures")
        self.assertIn("recursion", result.vocabulary)
        self.assertIn("functions", result.prerequisites)

    def test_formula_extraction(self):
        text = "Consider the inline formula $E = mc^2$ and block formula $$\\int x dx$$."
        result = asyncio.run(self.processor.process(text))
        
        self.assertIn("E = mc^2", result.extracted_formulas)
        self.assertIn("\\int x dx", result.extracted_formulas)
        
        # Verify validation stubs are called
        self.assertTrue(any(vf["formula"] == "E = mc^2" and vf["valid"] for vf in result.validated_formulas))

if __name__ == "__main__":
    unittest.main()
