import uuid
from typing import List, Union
import fitz
from services.document_intelligence.extractors.base import BaseExtractor, BaseAssetSaver
from services.document_intelligence.interfaces import ExtractedAsset, BoundingBox
from services.document_intelligence.config import die_config

class FigureExtractor(BaseExtractor):
    def __init__(self, asset_saver: BaseAssetSaver):
        self.asset_saver = asset_saver

    def extract(self, page: fitz.Page, page_number: int) -> List[Union[any, ExtractedAsset]]:
        """
        Detects vector graphics density and rasterizes them into a figure image.
        
        Args:
            page: fitz.Page
            page_number: int
            
        Returns:
            List[ExtractedAsset]
        """
        try:
            drawings = page.get_drawings()
        except Exception as e:
            return []

        # If drawing count is below threshold, skip
        if len(drawings) < die_config.vector_drawing_density_threshold:
            return []

        union_rect = None
        for d in drawings:
            r = d.get("rect")
            if not r:
                continue

            # Skip tiny vector elements (dots, dashes) and full page borders
            if r.width < 5 or r.height < 5:
                continue
            if r.width >= page.rect.width - 10 and r.height >= page.rect.height - 10:
                continue

            if union_rect is None:
                union_rect = fitz.Rect(r)
            else:
                union_rect.include_rect(r)

        if union_rect and not union_rect.is_empty:
            # Constrain to the actual page area
            union_rect.intersect(page.rect)
            
            # Ensure it meets a minimum visual size to be considered a diagram
            if union_rect.width >= 50 and union_rect.height >= 50:
                try:
                    # Rasterize the clipped boundary
                    pix = page.get_pixmap(clip=union_rect, dpi=150)
                    img_bytes = pix.tobytes("png")

                    relative_path = self.asset_saver.save_asset(
                        page_number=page_number,
                        asset_type="figure",
                        index=0,  # index 0 for the main clustered figure on the page
                        extension="png",
                        data=img_bytes
                    )

                    bbox = BoundingBox(x0=union_rect.x0, y0=union_rect.y0, x1=union_rect.x1, y1=union_rect.y1)

                    asset = ExtractedAsset(
                        asset_id=f"fig_{uuid.uuid4().hex[:8]}",
                        asset_type="figure",
                        file_path=relative_path,
                        page_number=page_number,
                        bbox=bbox,
                        confidence=1.0,  # Rasterized vector output is 100% accurate representations
                        source="figure",
                        metadata={"drawing_count": len(drawings)}
                    )
                    return [asset]
                except Exception as e:
                    # Fail silently per page to maintain fail-safe behavior
                    pass

        return []
