import unittest
from services.presentation.factory import PresentationPresenterFactory

class TestPresentationFactory(unittest.TestCase):
    def test_factory_default(self):
        cfg = PresentationPresenterFactory.create_config()
        self.assertEqual(cfg.duration_seconds, 3600)
        self.assertEqual(cfg.view_mode, "standard")

# Dynamically add 45 test cases to verify different duration configuration increments
for i in range(45):
    def make_test(duration):
        def test_func(self):
            cfg = PresentationPresenterFactory.create_config(duration=duration)
            self.assertEqual(cfg.duration_seconds, duration)
        return test_func
    setattr(TestPresentationFactory, f"test_factory_duration_{300 + i * 10}", make_test(300 + i * 10))

if __name__ == "__main__":
    unittest.main()
