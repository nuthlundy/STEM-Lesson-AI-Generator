import unittest
import os
import shutil
from services.document_intelligence.utils.asset_manager import AssetManager

class TestAssetManager(unittest.TestCase):
    def setUp(self):
        self.test_base_dir = os.path.abspath("backend/tests/temp_jobs")
        self.job_id = "test-job-123"
        self.manager = AssetManager(job_id=self.job_id, base_dir=self.test_base_dir)

    def tearDown(self):
        if os.path.exists(self.test_base_dir):
            shutil.rmtree(self.test_base_dir)

    def test_create_workspace(self):
        self.manager.create_job_workspace()
        job_dir = self.manager.get_job_dir()
        assets_dir = self.manager.get_assets_dir()
        
        self.assertTrue(os.path.exists(job_dir))
        self.assertTrue(os.path.exists(assets_dir))

    def test_save_asset(self):
        data = b"dummy image bytes"
        relative_path = self.manager.save_asset(
            page_number=2,
            asset_type="image",
            index=1,
            extension="png",
            data=data
        )
        
        # Verify returned relative path
        self.assertEqual(relative_path, "assets/test-job-123_page2_image_1.png")
        
        # Verify physical file existence
        absolute_path = os.path.join(self.manager.get_job_dir(), relative_path)
        self.assertTrue(os.path.exists(absolute_path))
        with open(absolute_path, "rb") as f:
            self.assertEqual(f.read(), data)

    def test_clean_workspace(self):
        self.manager.create_job_workspace()
        job_dir = self.manager.get_job_dir()
        self.assertTrue(os.path.exists(job_dir))
        
        self.manager.clean_job_workspace()
        self.assertFalse(os.path.exists(job_dir))

if __name__ == "__main__":
    unittest.main()
