import uuid
from typing import List, Union
import fitz
from services.document_intelligence.extractors.base import BaseExtractor
from services.document_intelligence.interfaces import DocumentBlock, BoundingBox

class NativePDFExtractor(BaseExtractor):
    def __init__(self, heading_threshold: float = 16.0):
        self.heading_threshold = heading_threshold

    def extract(self, page: fitz.Page, page_number: int) -> List[Union[DocumentBlock, any]]:
        """
        Extracts structured text blocks from a page.
        
        Args:
            page: fitz.Page
            page_number: int
            
        Returns:
            List[DocumentBlock]
        """
        blocks: List[DocumentBlock] = []
        try:
            text_dict = page.get_text("dict")
        except Exception as e:
            # If get_text fails, return empty so engine can fallback or handle it
            return []

        for raw_block in text_dict.get("blocks", []):
            # Only process text blocks (type 0)
            if raw_block.get("type") != 0:
                continue

            block_text = ""
            font_sizes = []
            font_names = []
            is_list_candidate = False

            lines = raw_block.get("lines", [])
            if not lines:
                continue

            for line in lines:
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    block_text += text
                    font_sizes.append(span.get("size", 10.0))
                    font_names.append(span.get("font", "unknown"))

            # Normalize text and strip excess whitespace
            block_text = block_text.strip()
            if not block_text:
                continue

            # Classify block type
            avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 10.0
            max_font_size = max(font_sizes) if font_sizes else 10.0
            primary_font = font_names[0] if font_names else "unknown"

            # Heuristics for lists
            first_char = block_text[0] if block_text else ""
            if first_char in ["•", "-", "*", "▪", "◦"]:
                block_type = "list"
            elif first_char.isdigit() and (block_text.startswith(first_char + ".") or block_text.startswith(first_char + ")")):
                block_type = "list"
            elif max_font_size >= self.heading_threshold:
                block_type = "heading"
            else:
                block_type = "paragraph"

            # Create bounding box
            x0, y0, x1, y1 = raw_block.get("bbox", (0, 0, 0, 0))
            bbox = BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1)

            # Metadata properties
            metadata = {
                "font_name": primary_font,
                "font_size": avg_font_size,
                "max_font_size": max_font_size,
                "is_bold": "bold" in primary_font.lower() or "black" in primary_font.lower()
            }

            block = DocumentBlock(
                block_id=f"blk_{uuid.uuid4().hex[:8]}",
                block_type=block_type,
                text=block_text,
                page_number=page_number,
                bbox=bbox,
                confidence=1.0,  # Native text extraction is considered fully accurate (100% confidence)
                source="native_pdf",
                metadata=metadata
            )
            blocks.append(block)

        return blocks
