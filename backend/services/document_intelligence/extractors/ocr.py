import os
import uuid
import io
from typing import List, Union
import fitz
import numpy as np
import cv2
import PIL.Image
import pytesseract

from services.document_intelligence.extractors.base import BaseExtractor
from services.document_intelligence.interfaces import DocumentBlock, BoundingBox
from services.document_intelligence.config import die_config

# Set Tesseract binary path on Windows if it exists
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    tessdata_dir = r"C:\Program Files\Tesseract-OCR\tessdata"
    if os.path.exists(tessdata_dir):
        os.environ["TESSDATA_PREFIX"] = tessdata_dir

class OCRExtractor(BaseExtractor):
    def __init__(self, dpi: int = 150):
        self.dpi = dpi

    def extract(self, page: fitz.Page, page_number: int) -> List[Union[DocumentBlock, any]]:
        """
        Renders the page to an image and runs layout-aware OCR.
        
        Args:
            page: fitz.Page
            page_number: int
            
        Returns:
            List[DocumentBlock]
        """
        blocks: List[DocumentBlock] = []
        try:
            # 1. Render page to image
            pix = page.get_pixmap(dpi=self.dpi)
            img_bytes = pix.tobytes("png")
            
            # Read image using PIL
            pil_img = PIL.Image.open(io.BytesIO(img_bytes))
            
            # 2. Run pytesseract image_to_data to get word-level coordinates and confidence
            data = pytesseract.image_to_data(pil_img, lang=die_config.ocr_lang, output_type=pytesseract.Output.DICT)
        except Exception as e:
            # Return empty list in case of errors, failing gracefully per page
            return []

        # Coordinate scaling factors: image pixels -> PDF points
        page_width = page.rect.width
        page_height = page.rect.height
        img_width, img_height = pil_img.size
        
        scale_x = page_width / img_width if img_width > 0 else 1.0
        scale_y = page_height / img_height if img_height > 0 else 1.0

        # Group words by block_num and par_num to reconstruct paragraphs
        grouped_blocks = {}
        
        n_items = len(data.get("text", []))
        for i in range(n_items):
            text = str(data["text"][i]).strip()
            conf = float(data["conf"][i])
            
            # Ignore empty/whitespace-only results and non-word elements (conf is -1)
            if not text or conf < 0:
                continue
                
            block_num = data["block_num"][i]
            par_num = data["par_num"][i]
            key = (block_num, par_num)
            
            left = data["left"][i]
            top = data["top"][i]
            width = data["width"][i]
            height = data["height"][i]
            
            # Convert to PDF coordinates
            x0 = left * scale_x
            y0 = top * scale_y
            x1 = (left + width) * scale_x
            y1 = (top + height) * scale_y
            
            if key not in grouped_blocks:
                grouped_blocks[key] = {
                    "texts": [text],
                    "confs": [conf],
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1
                }
            else:
                grouped_blocks[key]["texts"].append(text)
                grouped_blocks[key]["confs"].append(conf)
                grouped_blocks[key]["x0"] = min(grouped_blocks[key]["x0"], x0)
                grouped_blocks[key]["y0"] = min(grouped_blocks[key]["y0"], y0)
                grouped_blocks[key]["x1"] = max(grouped_blocks[key]["x1"], x1)
                grouped_blocks[key]["y1"] = max(grouped_blocks[key]["y1"], y1)

        # Build DocumentBlock list
        for (block_num, par_num), item in grouped_blocks.items():
            text_content = " ".join(item["texts"]).strip()
            if not text_content:
                continue
                
            # Average confidence score (convert 0-100 to 0.0-1.0)
            avg_conf = (sum(item["confs"]) / len(item["confs"])) / 100.0 if item["confs"] else 0.0
            
            # Ensure confidence is within boundaries
            avg_conf = max(0.0, min(1.0, avg_conf))

            bbox = BoundingBox(
                x0=item["x0"],
                y0=item["y0"],
                x1=item["x1"],
                y1=item["y1"]
            )
            
            block = DocumentBlock(
                block_id=f"blk_ocr_{uuid.uuid4().hex[:8]}",
                block_type="paragraph",
                text=text_content,
                page_number=page_number,
                bbox=bbox,
                confidence=avg_conf,
                source="ocr",
                metadata={"block_num": block_num, "par_num": par_num}
            )
            blocks.append(block)

        return blocks
