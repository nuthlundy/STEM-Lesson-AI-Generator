import uuid
from typing import List, Union
import fitz
from services.document_intelligence.extractors.base import BaseExtractor
from services.document_intelligence.interfaces import DocumentBlock, BoundingBox

class TableExtractor(BaseExtractor):
    def extract(self, page: fitz.Page, page_number: int) -> List[Union[any, DocumentBlock]]:
        """
        Detects vector grids and converts tables into markdown format.
        
        Args:
            page: fitz.Page
            page_number: int
            
        Returns:
            List[DocumentBlock]
        """
        blocks: List[DocumentBlock] = []
        try:
            # PyMuPDF built-in table finder
            tables = page.find_tables()
        except Exception as e:
            return []

        for index, table in enumerate(tables):
            try:
                cell_data = table.extract()
                if not cell_data or not cell_data[0]:
                    continue

                # Convert grid cells to a clean markdown table
                markdown_lines = []
                for row_idx, row in enumerate(cell_data):
                    # Clean and sanitize cell text
                    cleaned_row = [str(cell or "").replace("\n", " ").strip() for cell in row]
                    markdown_lines.append("| " + " | ".join(cleaned_row) + " |")
                    
                    # Add markdown header separator after the first row
                    if row_idx == 0:
                        separator = ["---"] * len(row)
                        markdown_lines.append("| " + " | ".join(separator) + " |")

                markdown_table = "\n".join(markdown_lines)
                
                # Table bounding box
                x0, y0, x1, y1 = table.bbox
                bbox = BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1)

                block = DocumentBlock(
                    block_id=f"tab_{uuid.uuid4().hex[:8]}",
                    block_type="table",
                    text=markdown_table,
                    page_number=page_number,
                    bbox=bbox,
                    confidence=1.0,  # Grid-based parsing is exact
                    source="table",
                    metadata={
                        "rows": len(cell_data),
                        "cols": len(cell_data[0]) if cell_data else 0,
                        "table_index": index
                    }
                )
                blocks.append(block)
            except Exception as e:
                # Skip corrupt tables on the page and continue
                continue

        return blocks
