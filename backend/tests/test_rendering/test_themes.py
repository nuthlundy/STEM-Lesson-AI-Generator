import unittest
from services.rendering.themes import get_theme, THEMES

class TestThemeEngine(unittest.TestCase):
    def test_all_themes_present(self):
        expected_keys = [
            "default", "academic", "minimal", "stem", "corporate",
            "modern", "dark", "light", "education", "science",
            "mathematics", "technology", "engineering"
        ]
        for key in expected_keys:
            self.assertIn(key, THEMES)

    def test_theme_properties(self):
        for name, cls in THEMES.items():
            theme = cls()
            styles = theme.get_styles()
            self.assertIn("colors", styles)
            self.assertIn("typography", styles)
            self.assertIn("primary", styles["colors"])
            self.assertIn("background", styles["colors"])

    def test_get_theme_resolver(self):
        theme = get_theme("stem")
        self.assertEqual(theme.get_styles()["colors"]["accent"], "#00D4B2")
        
        fallback = get_theme("non-existent-theme-abc")
        self.assertEqual(fallback.get_styles()["colors"]["accent"], "#0066CC")

if __name__ == "__main__":
    unittest.main()
