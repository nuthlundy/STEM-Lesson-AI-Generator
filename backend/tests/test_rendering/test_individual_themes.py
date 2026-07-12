import unittest
from services.rendering.themes.default import DefaultTheme
from services.rendering.themes.academic import AcademicTheme
from services.rendering.themes.minimal import MinimalTheme
from services.rendering.themes.stem import StemTheme
from services.rendering.themes.corporate import CorporateTheme
from services.rendering.themes.modern import ModernTheme
from services.rendering.themes.dark import DarkTheme
from services.rendering.themes.light import LightTheme
from services.rendering.themes.education import EducationTheme
from services.rendering.themes.science import ScienceTheme
from services.rendering.themes.mathematics import MathematicsTheme
from services.rendering.themes.technology import TechnologyTheme
from services.rendering.themes.engineering import EngineeringTheme

class TestIndividualThemes(unittest.TestCase):
    # Font tests
    def test_default_theme_font(self):
        self.assertIn("sans-serif", DefaultTheme().get_styles()["typography"]["font_family"])

    def test_academic_theme_font(self):
        self.assertIn("serif", AcademicTheme().get_styles()["typography"]["font_family"])

    def test_minimal_theme_font(self):
        self.assertIn("monospace", MinimalTheme().get_styles()["typography"]["font_family"])

    def test_stem_theme_font(self):
        self.assertIn("sans-serif", StemTheme().get_styles()["typography"]["font_family"])

    def test_corporate_theme_font(self):
        self.assertIn("sans-serif", CorporateTheme().get_styles()["typography"]["font_family"])

    def test_modern_theme_font(self):
        self.assertIn("sans-serif", ModernTheme().get_styles()["typography"]["font_family"])

    def test_dark_theme_font(self):
        self.assertIn("sans-serif", DarkTheme().get_styles()["typography"]["font_family"])

    def test_light_theme_font(self):
        self.assertIn("sans-serif", LightTheme().get_styles()["typography"]["font_family"])

    def test_education_theme_font(self):
        self.assertIn("sans-serif", EducationTheme().get_styles()["typography"]["font_family"])

    def test_science_theme_font(self):
        self.assertIn("sans-serif", ScienceTheme().get_styles()["typography"]["font_family"])

    def test_mathematics_theme_font(self):
        self.assertIn("serif", MathematicsTheme().get_styles()["typography"]["font_family"])

    def test_technology_theme_font(self):
        self.assertIn("monospace", TechnologyTheme().get_styles()["typography"]["font_family"])

    def test_engineering_theme_font(self):
        self.assertIn("sans-serif", EngineeringTheme().get_styles()["typography"]["font_family"])

    # Background color tests
    def test_default_theme_bg(self):
        self.assertEqual(DefaultTheme().get_styles()["colors"]["background"], "#FFFFFF")

    def test_academic_theme_bg(self):
        self.assertEqual(AcademicTheme().get_styles()["colors"]["background"], "#F2F2F2")

    def test_minimal_theme_bg(self):
        self.assertEqual(MinimalTheme().get_styles()["colors"]["background"], "#FDFDFD")

    def test_stem_theme_bg(self):
        self.assertEqual(StemTheme().get_styles()["colors"]["background"], "#F4F6F8")

    def test_corporate_theme_bg(self):
        self.assertEqual(CorporateTheme().get_styles()["colors"]["background"], "#F8FAFC")

    def test_modern_theme_bg(self):
        self.assertEqual(ModernTheme().get_styles()["colors"]["background"], "#f8fafc")

    def test_dark_theme_bg(self):
        self.assertEqual(DarkTheme().get_styles()["colors"]["background"], "#0F172A")

    def test_light_theme_bg(self):
        self.assertEqual(LightTheme().get_styles()["colors"]["background"], "#FFFFFF")

    def test_education_theme_bg(self):
        self.assertEqual(EducationTheme().get_styles()["colors"]["background"], "#F9FAFB")

    def test_science_theme_bg(self):
        self.assertEqual(ScienceTheme().get_styles()["colors"]["background"], "#ECFDF5")

    def test_mathematics_theme_bg(self):
        self.assertEqual(MathematicsTheme().get_styles()["colors"]["background"], "#F5F3FF")

    def test_technology_theme_bg(self):
        self.assertEqual(TechnologyTheme().get_styles()["colors"]["background"], "#020617")

    def test_engineering_theme_bg(self):
        self.assertEqual(EngineeringTheme().get_styles()["colors"]["background"], "#FFF7ED")

    # Spacing and border tests
    def test_stem_padding(self):
        self.assertEqual(StemTheme().get_styles()["spacing"]["padding"], 12)

    def test_minimal_padding(self):
        self.assertEqual(MinimalTheme().get_styles()["spacing"]["padding"], 8)

    def test_academic_radius(self):
        self.assertEqual(AcademicTheme().get_styles()["borders"]["radius"], 0)

    def test_modern_radius(self):
        self.assertEqual(ModernTheme().get_styles()["borders"]["radius"], 8)

if __name__ == "__main__":
    unittest.main()
