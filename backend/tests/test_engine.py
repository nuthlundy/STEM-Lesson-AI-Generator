import unittest
import os
import shutil
import fitz
import PIL.Image
import io
import json

from services.document_intelligence.engine import DocumentIntelligenceEngine

class TestDocumentIntelligenceEngine(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.test_base_dir = os.path.abspath("backend/tests/temp_jobs_engine")
        os.makedirs(self.test_base_dir, exist_ok=True)
        
        self.pdf_path = os.path.join(self.test_base_dir, "test_input.pdf")
        self.job_id = "engine-test-job-99"
        self.original_filename = "test_input.pdf"

        # Create a physical PDF document with distinct content classes
        doc = fitz.open()
        
        # Page 1: Native Text and Math
        page1 = doc.new_page(width=600, height=800)
        page1.insert_text((50, 50), "Lesson Title: Physics Mechanics", fontsize=20, fontname="hebo")
        page1.insert_text((50, 100), "Newtonian gravity describes the force between two masses.", fontsize=11, fontname="helv")
        page1.insert_text((50, 150), "Equation: F = G * \\frac{m1 * m2}{r^2}", fontsize=11, fontname="helv")

        # Page 2: Table grid
        page2 = doc.new_page(width=600, height=800)
        # Add descriptive text to exceed character threshold (50+) and prevent OCR trigger
        page2.insert_text((50, 50), "Table 1.1: Physical measurements of specimen masses in the experimental laboratory.", fontsize=11, fontname="helv")
        
        # Draw horizontal lines for table
        for y in [100, 130, 160, 190]:
            page2.draw_line(fitz.Point(50, y), fitz.Point(250, y), color=(0, 0, 0), width=1)
        # Draw vertical lines
        for x in [50, 116, 183, 250]:
            page2.draw_line(fitz.Point(x, 100), fitz.Point(x, 190), color=(0, 0, 0), width=1)
        page2.insert_text((60, 120), "Col1", fontsize=10, fontname="helv")
        page2.insert_text((126, 120), "Col2", fontsize=10, fontname="helv")
        page2.insert_text((193, 120), "Col3", fontsize=10, fontname="helv")
        page2.insert_text((60, 150), "Val1", fontsize=10, fontname="helv")
        page2.insert_text((126, 150), "Val2", fontsize=10, fontname="helv")
        page2.insert_text((193, 150), "Val3", fontsize=10, fontname="helv")

        # Page 3: Image element
        page3 = doc.new_page(width=600, height=800)
        img = PIL.Image.new("RGB", (150, 150), color="blue")
        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        page3.insert_image(fitz.Rect(50, 50, 200, 200), stream=img_io.getvalue())

        doc.save(self.pdf_path)
        doc.close()

        self.engine = DocumentIntelligenceEngine(
            job_id=self.job_id,
            file_path=self.pdf_path,
            original_filename=self.original_filename,
            base_dir=self.test_base_dir
        )

    def tearDown(self):
        if os.path.exists(self.test_base_dir):
            shutil.rmtree(self.test_base_dir)

    async def test_complete_engine_pipeline(self):
        progress_reports = []

        def progress_callback(percent: int, message: str):
            progress_reports.append((percent, message))

        # Run pipeline
        lesson_json_path = await self.engine.process(progress_callback=progress_callback)

        # Assert output path
        self.assertTrue(os.path.exists(lesson_json_path))
        self.assertEqual(os.path.basename(lesson_json_path), "lesson.json")

        # Load generated lesson.json and validate structure
        with open(lesson_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate top-level schema fields
        self.assertIn("metadata", data)
        self.assertIn("blocks", data)
        self.assertIn("assets", data)
        self.assertIn("metrics", data)

        metadata = data["metadata"]
        self.assertEqual(metadata["job_id"], self.job_id)
        self.assertEqual(metadata["schema_version"], "1.0.0")
        self.assertEqual(metadata["total_pages"], 3)

        blocks = data["blocks"]
        # Verify that we extracted headings, equations, and tables
        block_types = [b["block_type"] for b in blocks]
        self.assertIn("heading", block_types)
        self.assertIn("equation", block_types)
        self.assertIn("table", block_types)

        # Validate that all blocks have confidence scores and source fields
        for block in blocks:
            self.assertIn("confidence", block)
            self.assertIn("source", block)
            self.assertGreater(block["confidence"], 0.0)

        # Validate image extraction
        assets = data["assets"]
        self.assertEqual(len(assets), 1)
        self.assertEqual(assets[0]["asset_type"], "image")
        self.assertEqual(assets[0]["source"], "image")
        self.assertIn("confidence", assets[0])
        self.assertEqual(assets[0]["confidence"], 1.0)

        # Verify progress reports were emitted
        self.assertGreater(len(progress_reports), 0)
        self.assertEqual(progress_reports[-1][0], 100)

if __name__ == "__main__":
    unittest.main()
