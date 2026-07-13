import unittest
from services.presentation.optimizer.optimizer import PresentationOptimizer
from services.presentation.schemas import PresentationSessionModel

class TestPresentationOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = PresentationOptimizer()
        self.session = PresentationSessionModel(
            session_id="session-opt",
            presentation_path="lesson.pptx",
            duration_seconds=3600,
            slides=[]
        )

    def test_optimizer_output_keys(self):
        res = self.optimizer.optimize(self.session)
        self.assertIn("duplicate_assets_removed", res)
        self.assertIn("unused_resources_removed", res)
        self.assertIn("package_compression_ratio", res)
        self.assertIn("metadata_keys_compressed", res)

    def test_cleanup_duplicates(self):
        from services.presentation.optimizer.cleanup import ResourcesCleanup
        val = ResourcesCleanup.cleanup_duplicate_assets(self.session)
        self.assertEqual(val, 0)

    def test_cleanup_unused(self):
        from services.presentation.optimizer.cleanup import ResourcesCleanup
        val = ResourcesCleanup.cleanup_unused_resources(self.session)
        self.assertEqual(val, 0)

    def test_compression_ratio(self):
        from services.presentation.optimizer.compression import PackageCompression
        val = PackageCompression.compress_package(self.session)
        self.assertEqual(val, 1.0)

    def test_compression_metadata(self):
        from services.presentation.optimizer.compression import PackageCompression
        val = PackageCompression.compress_metadata(self.session)
        self.assertEqual(val, 0)

if __name__ == "__main__":
    unittest.main()
