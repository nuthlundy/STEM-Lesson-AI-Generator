import unittest
import os
import shutil
import fitz
import PIL.Image
import io

from services.document_intelligence.extractors.image import ImageExtractor
from services.document_intelligence.extractors.figure import FigureExtractor
from services.document_intelligence.utils.asset_manager import AssetManager

class TestImageFigureExtractors(unittest.TestCase):
    def setUp(self):
        self.test_base_dir = os.path.abspath("backend/tests/temp_jobs_media")
        self.job_id = "test-job-media"
        self.asset_manager = AssetManager(job_id=self.job_id, base_dir=self.test_base_dir)
        self.asset_manager.create_job_workspace()

        # Create in-memory document
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=600, height=800)

        # 1. Insert a mock raster image (red square, 200x200)
        img = PIL.Image.new("RGB", (200, 200), color="red")
        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_bytes = img_io.getvalue()
        self.page.insert_image(fitz.Rect(50, 50, 250, 250), stream=img_bytes)

        # 2. Insert vector drawings (20 rects) to trigger FigureExtractor density threshold
        for i in range(20):
            self.page.draw_rect(fitz.Rect(50, 400 + i*5, 250, 450 + i*5), color=(1, 0, 0), width=1)

    def tearDown(self):
        self.doc.close()
        if os.path.exists(self.test_base_dir):
            shutil.rmtree(self.test_base_dir)

    def test_image_extractor(self):
        extractor = ImageExtractor(self.asset_manager)
        assets = extractor.extract(self.page, page_number=1)

        self.assertEqual(len(assets), 1)
        self.assertEqual(assets[0].asset_type, "image")
        self.assertEqual(assets[0].source, "image")
        self.assertEqual(assets[0].confidence, 1.0)
        self.assertTrue(os.path.exists(os.path.join(self.test_base_dir, self.job_id, assets[0].file_path)))

    def test_figure_extractor(self):
        extractor = FigureExtractor(self.asset_manager)
        assets = extractor.extract(self.page, page_number=1)

        self.assertEqual(len(assets), 1)
        self.assertEqual(assets[0].asset_type, "figure")
        self.assertEqual(assets[0].source, "figure")
        self.assertEqual(assets[0].confidence, 1.0)
        self.assertTrue(os.path.exists(os.path.join(self.test_base_dir, self.job_id, assets[0].file_path)))

if __name__ == "__main__":
    unittest.main()
