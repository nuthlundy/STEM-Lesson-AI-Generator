import unittest
import fitz
from services.document_intelligence.extractors.table import TableExtractor
from services.document_intelligence.extractors.equation import EquationExtractor
from services.document_intelligence.interfaces import DocumentBlock

class TestTableEquationExtractors(unittest.TestCase):
    def setUp(self):
        # Create in-memory document
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=600, height=800)

        # 1. Construct a vector grid table
        # Draw horizontal lines
        for y in [100, 130, 160, 190]:
            self.page.draw_line(fitz.Point(50, y), fitz.Point(250, y), color=(0, 0, 0), width=1)
        # Draw vertical lines
        for x in [50, 116, 183, 250]:
            self.page.draw_line(fitz.Point(x, 100), fitz.Point(x, 190), color=(0, 0, 0), width=1)

        # Insert table cell texts
        self.page.insert_text((60, 120), "Col1", fontsize=10, fontname="helv")
        self.page.insert_text((126, 120), "Col2", fontsize=10, fontname="helv")
        self.page.insert_text((193, 120), "Col3", fontsize=10, fontname="helv")
        self.page.insert_text((60, 150), "Val1", fontsize=10, fontname="helv")
        self.page.insert_text((126, 150), "Val2", fontsize=10, fontname="helv")
        self.page.insert_text((193, 150), "Val3", fontsize=10, fontname="helv")

        # 2. Insert mathematical equation block
        self.page.insert_text((50, 300), "Formula: E = mc^2 + \\int_a^b f(x) dx", fontsize=12, fontname="helv")
        self.page.insert_text((50, 350), "Relation: \\alpha + \\beta = \\theta", fontsize=12, fontname="helv")

    def tearDown(self):
        self.doc.close()

    def test_table_extractor(self):
        extractor = TableExtractor()
        blocks = extractor.extract(self.page, page_number=1)

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, "table")
        self.assertEqual(blocks[0].source, "table")
        self.assertIn("Col1 | Col2 | Col3", blocks[0].text)
        self.assertIn("Val1 | Val2 | Val3", blocks[0].text)

    def test_equation_extractor(self):
        extractor = EquationExtractor()
        blocks = extractor.extract(self.page, page_number=1)

        self.assertGreaterEqual(len(blocks), 1)
        # Verify at least one equation block is found
        eq_blocks = [b for b in blocks if b.block_type == "equation"]
        self.assertGreaterEqual(len(eq_blocks), 1)
        self.assertEqual(eq_blocks[0].source, "equation")
        self.assertTrue(
            "int" in eq_blocks[0].text or "alpha" in eq_blocks[0].text or "mc^2" in eq_blocks[0].text or "Relation" in eq_blocks[0].text
        )

if __name__ == "__main__":
    unittest.main()
