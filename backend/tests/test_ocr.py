import unittest
import fitz
from services.document_intelligence.extractors.ocr import OCRExtractor
from services.document_intelligence.interfaces import DocumentBlock

class TestOCRExtractor(unittest.TestCase):
    def setUp(self):
        # Create an in-memory PDF using PyMuPDF
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=600, height=800)
        
        # Write some clear text that Tesseract can OCR easily
        self.page.insert_text((50, 100), "Tesseract OCR Test Page", fontsize=24, fontname="hebo")
        self.page.insert_text((50, 200), "This is a paragraph extracted via OCR engine.", fontsize=14, fontname="helv")
        
        self.extractor = OCRExtractor(dpi=150)

    def tearDown(self):
        self.doc.close()

    def test_extract_ocr(self):
        blocks = self.extractor.extract(self.page, page_number=1)
        
        # Ensure we got blocks back
        self.assertGreaterEqual(len(blocks), 1)
        
        # Check properties of the first major block
        found_test_text = False
        for block in blocks:
            if "tesseract" in block.text.lower() or "ocr" in block.text.lower():
                found_test_text = True
                self.assertEqual(block.source, "ocr")
                self.assertGreater(block.confidence, 0.0)
                self.assertLessEqual(block.confidence, 1.0)
                self.assertIsNotNone(block.bbox)
                self.assertEqual(block.block_type, "paragraph")
                
        self.assertTrue(found_test_text, "OCR failed to read the test page text")

if __name__ == "__main__":
    unittest.main()
