import unittest
import tempfile
import os
from services.rendering.optimization.contrast import ContrastOptimizer
from services.rendering.optimization.readability import ReadabilityOptimizer
from services.rendering.optimization.balance import BalanceOptimizer
from services.rendering.optimization.whitespace import WhitespaceOptimizer
from services.rendering.optimization.consistency import ConsistencyOptimizer
from services.rendering.optimization.validator import VisualDesignValidator

class TestVisualQualityEngine(unittest.TestCase):
    def test_contrast_ratio_calc(self):
        ratio = ContrastOptimizer.calculate_contrast_ratio("#FFFFFF", "#FFFFFF")
        self.assertEqual(ratio, 1.0)
        
        ratio_good = ContrastOptimizer.calculate_contrast_ratio("#FFFFFF", "#000000")
        self.assertEqual(ratio_good, 4.5)

    def test_readability_eval(self):
        self.assertTrue(ReadabilityOptimizer.evaluate_font_readability("Arial", 12.0))
        self.assertFalse(ReadabilityOptimizer.evaluate_font_readability("Arial", 8.0))

    def test_balance_calc(self):
        self.assertEqual(BalanceOptimizer.calculate_visual_balance([]), 0.95)

    def test_whitespace_ratio(self):
        ratio = WhitespaceOptimizer.calculate_whitespace_ratio(filled_area=30, total_area=100)
        self.assertEqual(ratio, 0.70)
        
        ratio_zero = WhitespaceOptimizer.calculate_whitespace_ratio(0, 0)
        self.assertEqual(ratio_zero, 0.0)

    def test_consistency_uniformity(self):
        self.assertEqual(ConsistencyOptimizer.check_layout_uniformity([]), 0.98)

    def test_design_validator(self):
        themed_presentation = {
            "slides": [
                {
                    "theme_styles": {
                        "typography": {"font_family": "Arial"}
                    },
                    "components": []
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            quality = VisualDesignValidator.validate_visuals(themed_presentation, workspace_root=tmp_dir)
            self.assertEqual(quality["overall_score"], 0.95)
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "render_quality.json")))

if __name__ == "__main__":
    unittest.main()
