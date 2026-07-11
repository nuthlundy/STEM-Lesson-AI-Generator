import os
import json
import time
import fitz
from typing import List, Optional, Callable
from services.document_intelligence.interfaces import (
    DocumentIntelligenceResult,
    DocumentMetadata,
    DocumentBlock,
    ExtractedAsset,
    ProcessingMetrics
)
from services.document_intelligence.config import die_config
from services.document_intelligence.utils.asset_manager import AssetManager
from services.document_intelligence.utils.logger import DIELogger
from services.document_intelligence.extractors.native_pdf import NativePDFExtractor
from services.document_intelligence.extractors.ocr import OCRExtractor
from services.document_intelligence.extractors.image import ImageExtractor
from services.document_intelligence.extractors.figure import FigureExtractor
from services.document_intelligence.extractors.table import TableExtractor
from services.document_intelligence.extractors.equation import EquationExtractor

class DocumentIntelligenceEngine:
    def __init__(self, job_id: str, file_path: str, original_filename: str, base_dir: str = "uploads/jobs"):
        self.job_id = job_id
        self.file_path = file_path
        self.original_filename = original_filename
        
        self.asset_manager = AssetManager(job_id=job_id, base_dir=base_dir)
        self.logger = DIELogger(job_id)
        
        # Instantiate extractors
        self.native_extractor = NativePDFExtractor()
        self.ocr_extractor = OCRExtractor()
        self.image_extractor = ImageExtractor(self.asset_manager)
        self.figure_extractor = FigureExtractor(self.asset_manager)
        self.table_extractor = TableExtractor()
        self.equation_extractor = EquationExtractor()

    def _resolve_overlapping_blocks(self, blocks: List[DocumentBlock]) -> List[DocumentBlock]:
        """
        Deduplicates paragraphs that are already captured by more specialized
        blocks (like tables and equations) to prevent text duplication in lesson.json.
        """
        special_blocks = [b for b in blocks if b.block_type in ("table", "equation")]
        paragraphs = [b for b in blocks if b.block_type not in ("table", "equation")]
        
        filtered_paragraphs = []
        for p in paragraphs:
            is_duplicate = False
            for s in special_blocks:
                # 1. Text-based substring check
                if p.text in s.text:
                    is_duplicate = True
                    break
                
                # 2. Bounding box intersection check (if bboxes exist)
                if p.bbox and s.bbox:
                    p_box = fitz.Rect(p.bbox.x0, p.bbox.y0, p.bbox.x1, p.bbox.y1)
                    s_box = fitz.Rect(s.bbox.x0, s.bbox.y0, s.bbox.x1, s.bbox.y1)
                    
                    # If paragraph box is completely/mostly inside the special box, discard it
                    p_area = p_box.get_area()
                    if s_box.contains(p_box) or (p_area > 0 and p_box.intersect(s_box).get_area() / p_area > 0.5):
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                filtered_paragraphs.append(p)
                
        return special_blocks + filtered_paragraphs

    async def process(self, progress_callback: Optional[Callable[[int, str], None]] = None) -> str:
        """
        Orchestrates page extraction.
        Returns the absolute filepath to the generated lesson.json.
        """
        start_time = time.time()
        self.logger.info("Initializing Document Intelligence Engine pipeline.")
        self.asset_manager.create_job_workspace()

        all_blocks: List[DocumentBlock] = []
        all_assets: List[ExtractedAsset] = []
        requires_ocr_doc = False

        # Use context manager for robust resource cleanup and preventing file handle leaks
        try:
            with fitz.open(self.file_path) as doc:
                total_pages = len(doc)

                # Page-by-page extraction loop
                for page_idx in range(total_pages):
                    page_num = page_idx + 1
                    self.logger.info("Processing page started", page=page_num)
                    
                    if progress_callback:
                        progress_callback(int((page_idx / total_pages) * 100), f"Extracting page {page_num} of {total_pages}")

                    try:
                        page = doc[page_idx]
                        
                        # 1. OCR Decision Logic Heuristic
                        raw_text = page.get_text()
                        needs_ocr = len(raw_text.strip()) < die_config.min_chars_per_page
                        
                        page_blocks: List[DocumentBlock] = []
                        page_assets: List[ExtractedAsset] = []

                        if needs_ocr:
                            self.logger.info("Page contains low native text density. Triggering OCR fallback.", page=page_num)
                            requires_ocr_doc = True
                            page_blocks.extend(self.ocr_extractor.extract(page, page_num))
                        else:
                            page_blocks.extend(self.native_extractor.extract(page, page_num))
                            page_blocks.extend(self.equation_extractor.extract(page, page_num))
                            page_blocks.extend(self.table_extractor.extract(page, page_num))

                        # Run Image and Figure extractors on all pages
                        page_assets.extend(self.image_extractor.extract(page, page_num))
                        page_assets.extend(self.figure_extractor.extract(page, page_num))

                        # Deduplicate paragraph blocks overlapping with tables/equations
                        deduplicated_blocks = self._resolve_overlapping_blocks(page_blocks)
                        
                        all_blocks.extend(deduplicated_blocks)
                        all_assets.extend(page_assets)
                        
                        self.logger.info(f"Page processing completed. Extracted {len(deduplicated_blocks)} blocks and {len(page_assets)} assets.", page=page_num)

                    except Exception as e:
                        # Fail Safe Design: Page failure isolation
                        self.logger.recoverable_error(f"Error occurred during page extraction: {e}", page=page_num)
                        continue
        except Exception as e:
            self.logger.fatal_error(f"Failed during PDF document handling: {e}")
            raise RuntimeError(f"Pipeline processing failed: {e}")
        
        # End Timing
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Update final progress
        if progress_callback:
            progress_callback(100, "Extraction pipeline completed.")

        # Create Metadata
        metadata = DocumentMetadata(
            job_id=self.job_id,
            original_filename=self.original_filename,
            total_pages=total_pages,
            processing_time_sec=elapsed_time,
            requires_ocr=requires_ocr_doc,
            schema_version="1.0.0"
        )

        # Create Metrics
        metrics = ProcessingMetrics(
            progress=100.0,
            execution_time=elapsed_time,
            warnings=self.logger.warnings,
            recoverable_errors=self.logger.recoverable_errors,
            fatal_errors=self.logger.fatal_errors
        )

        # Assemble Result
        result = DocumentIntelligenceResult(
            metadata=metadata,
            blocks=all_blocks,
            assets=all_assets,
            metrics=metrics
        )

        # Serialize to lesson.json
        job_dir = self.asset_manager.get_job_dir()
        lesson_json_path = os.path.join(job_dir, "lesson.json")
        
        try:
            with open(lesson_json_path, "w", encoding="utf-8") as f:
                f.write(result.model_dump_json(indent=2))
            self.logger.info(f"Successfully generated intermediate representation lesson.json at: {lesson_json_path}")
        except Exception as e:
            self.logger.fatal_error(f"Failed to serialize result to lesson.json: {e}")
            raise RuntimeError(f"Serialization failed: {e}")

        return os.path.abspath(lesson_json_path)
