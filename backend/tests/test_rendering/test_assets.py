import unittest
from services.rendering.assets.icons import IconLibrary
from services.rendering.assets.illustrations import IllustrationLibrary
from services.rendering.assets.backgrounds import BackgroundLibrary
from services.rendering.assets.placeholders import PlaceholderGenerator

class TestAssetLibrary(unittest.TestCase):
    def test_icon_lookup(self):
        icon = IconLibrary.lookup_icon("physics")
        self.assertEqual(icon, "atom-icon")
        
        fallback = IconLibrary.lookup_icon("unknown")
        self.assertEqual(fallback, "question-icon")

    def test_illustration_lookup(self):
        ill = IllustrationLibrary.get_illustration("math")
        self.assertEqual(ill, "geometry_vector.png")
        
        fallback = IllustrationLibrary.get_illustration("unknown")
        self.assertEqual(fallback, "generic_science_vector.png")

    def test_background_lookup(self):
        bg = BackgroundLibrary.get_background("dark")
        self.assertEqual(bg, "dark_particles.png")
        
        fallback = BackgroundLibrary.get_background("minimal")
        self.assertEqual(fallback, "solid_flat_background.png")

    def test_placeholder_generator(self):
        ph = PlaceholderGenerator.generate_placeholder(200, 150, "Test Label")
        self.assertIn("200x150", ph)
        self.assertIn("Test+Label", ph)

if __name__ == "__main__":
    unittest.main()
