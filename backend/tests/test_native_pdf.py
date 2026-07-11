import unittest
import fitz
from services.document_intelligence.extractors.native_pdf import NativePDFExtractor
from services.document_intelligence.interfaces import DocumentBlock

class TestNativePDFExtractor(unittest.TestCase):
    def setUp(self):
        # Create an in-memory PDF using PyMuPDF
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=600, height=800)
        
        # Insert test elements
        # 1. Heading
        self.page.insert_text((50, 50), "STEM Chemistry Lesson", fontsize=20, fontname="hebo")
        # 2. Paragraph
        self.page.insert_text((50, 100), "This lesson covers the fundamentals of atomic structure and molecular bonding.", fontsize=12, fontname="helv")
        # 3. List Item
        self.page.insert_text((50, 150), "- Protons and Neutrons reside in the nucleus.", fontsize=12, fontname="helv")
        
        self.extractor = NativePDFExtractor(heading_threshold=16.0)

    def tearDown(self):
        self.doc.close()

    def test_extract_blocks(self):
        blocks = self.extractor.extract(self.page, page_number=1)
        
        # Verify block count (should find at least 3 distinct blocks depending on PyMuPDF grouping)
        self.assertGreaterEqual(len(blocks), 3)
        
        # Verify structural classification
        headings = [b for b in blocks if b.block_type == "heading"]
        paragraphs = [b for b in blocks if b.block_type == "paragraph"]
        lists = [b for b in blocks if b.block_type == "list"]
        
        self.assertEqual(len(headings), 1)
        self.assertEqual(headings[0].text, "STEM Chemistry Lesson")
        self.assertEqual(headings[0].confidence, 1.0)
        self.assertEqual(headings[0].source, "native_pdf")
        
        self.assertEqual(len(paragraphs), 1)
        self.assertEqual(paragraphs[0].text, "This lesson covers the fundamentals of atomic structure and molecular bonding.")
        
        self.assertEqual(len(lists), 1)
        self.assertTrue(lists[0].text.startswith("-"))

if __name__ == "__main__":
    unittest.main()
