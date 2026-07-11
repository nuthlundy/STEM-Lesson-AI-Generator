import uuid
from typing import List, Union
import fitz
from services.document_intelligence.extractors.base import BaseExtractor
from services.document_intelligence.interfaces import DocumentBlock, BoundingBox
from services.document_intelligence.config import die_config

class EquationExtractor(BaseExtractor):
    def __init__(self, confidence_score: float = 1.0):
        self.confidence_score = confidence_score

    def extract(self, page: fitz.Page, page_number: int) -> List[Union[any, DocumentBlock]]:
        """
        Extracts mathematical equations based on font names and symbol heuristics.
        
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
            return []

        # Common math symbols to search for
        math_symbols = [
            "∫", "∑", "√", "π", "θ", "λ", "α", "β", "γ", "δ", "ε", "σ", "μ", "φ", "ψ", "ω", 
            "±", "≠", "≤", "≥", "≈", "∞", "×", "÷", "∈", "∉", "⊆", "⊇", "⊂", "⊃", "∪", "∩"
        ]

        for raw_block in text_dict.get("blocks", []):
            if raw_block.get("type") != 0:
                continue

            block_text = ""
            has_math_font = False
            has_math_symbol = False
            font_names = []

            lines = raw_block.get("lines", [])
            for line in lines:
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    block_text += text
                    
                    font = span.get("font", "").lower()
                    font_names.append(font)

                    # Check for math font identifiers
                    if any(ident in font for ident in die_config.math_font_identifiers):
                        has_math_font = True

            block_text = block_text.strip()
            if not block_text:
                continue

            # Check if block text contains explicit math symbols
            if any(sym in block_text for sym in math_symbols):
                has_math_symbol = True

            # Additional check: LaTeX format notation
            if "\\" in block_text and any(keyword in block_text for keyword in ["frac", "int", "sum", "alpha", "beta", "theta", "sqrt"]):
                has_math_symbol = True

            # If it qualifies as an equation block
            if has_math_font or has_math_symbol:
                x0, y0, x1, y1 = raw_block.get("bbox", (0, 0, 0, 0))
                bbox = BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1)

                block = DocumentBlock(
                    block_id=f"eq_{uuid.uuid4().hex[:8]}",
                    block_type="equation",
                    text=block_text,
                    page_number=page_number,
                    bbox=bbox,
                    confidence=self.confidence_score,
                    source="equation",
                    metadata={
                        "fonts": list(set(font_names)),
                        "detected_via_font": has_math_font,
                        "detected_via_symbol": has_math_symbol
                    }
                )
                blocks.append(block)

        return blocks
