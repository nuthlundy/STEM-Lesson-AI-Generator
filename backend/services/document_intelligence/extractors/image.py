import uuid
from typing import List, Union
import fitz
from services.document_intelligence.extractors.base import BaseExtractor, BaseAssetSaver
from services.document_intelligence.interfaces import ExtractedAsset, BoundingBox
from services.document_intelligence.config import die_config

class ImageExtractor(BaseExtractor):
    def __init__(self, asset_saver: BaseAssetSaver):
        self.asset_saver = asset_saver

    def extract(self, page: fitz.Page, page_number: int) -> List[Union[any, ExtractedAsset]]:
        """
        Extracts embedded raster images from the page.
        
        Args:
            page: fitz.Page
            page_number: int
            
        Returns:
            List[ExtractedAsset]
        """
        assets: List[ExtractedAsset] = []
        doc = page.parent  # Retrieve the fitz.Document parent

        try:
            image_info_list = page.get_images(full=True)
        except Exception as e:
            return []

        for index, img_info in enumerate(image_info_list):
            xref = img_info[0]
            width = img_info[2]
            height = img_info[3]

            # Filter out small images (logos, bullets, spacer graphics)
            if width < die_config.min_image_width or height < die_config.min_image_height:
                continue

            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue
                
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]  # e.g., "png", "jpeg"
                
                # Save the image bytes to our job assets directory via BaseAssetSaver
                relative_path = self.asset_saver.save_asset(
                    page_number=page_number,
                    asset_type="image",
                    index=index,
                    extension=image_ext,
                    data=image_bytes
                )
                
                # Retrieve bounding box on the page where image is placed
                rects = page.get_image_rects(xref)
                bbox = None
                if rects:
                    r = rects[0]
                    bbox = BoundingBox(x0=r.x0, y0=r.y0, x1=r.x1, y1=r.y1)

                asset = ExtractedAsset(
                    asset_id=f"img_{uuid.uuid4().hex[:8]}",
                    asset_type="image",
                    file_path=relative_path,
                    page_number=page_number,
                    bbox=bbox,
                    confidence=1.0,  # Extraction of raw binary is 100% accurate
                    source="image",
                    metadata={"width": width, "height": height, "xref": xref}
                )
                assets.append(asset)
            except Exception as e:
                # Fail page image extraction gracefully per image
                continue

        return assets
