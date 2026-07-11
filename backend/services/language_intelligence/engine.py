import os
import json
import time
import asyncio
from typing import Optional, Callable
from services.document_intelligence.interfaces import DocumentIntelligenceResult
from services.language_intelligence.interfaces import LanguageIntelligenceResult, EnrichedDocumentBlock
from services.language_intelligence.processors.factory import ProcessorFactory
from core.logger import get_logger

class LanguageIntelligenceEngine:
    def __init__(self, job_id: str, base_dir: str = "uploads/jobs"):
        self.job_id = job_id
        self.base_dir = base_dir
        self.job_dir = os.path.abspath(os.path.join(self.base_dir, self.job_id))
        self.input_file = os.path.join(self.job_dir, "lesson.json")
        self.output_file = os.path.join(self.job_dir, "lesson_language.json")
        
        self.logger = get_logger("stem_ai.lie.engine")
        
        # Instantiate semantic processor using the dynamic factory
        self.processor = ProcessorFactory.get_processor()

    async def _process_block(self, block) -> EnrichedDocumentBlock:
        # Pass non-text blocks through without AI semantic changes
        if block.block_type in ("image_ref", "table", "equation", "figure"):
            # For non-text blocks, apply deterministic processor to get baseline metadata quickly
            meta = await self.processor.deterministic_fallback.process(original_text=block.text, cleaned_text=block.text)
        else:
            meta = await self.processor.process(original_text=block.text)
            
        enriched = EnrichedDocumentBlock(
            block_id=block.block_id,
            block_type=block.block_type,
            text=block.text,
            page_number=block.page_number,
            bbox=block.bbox,
            confidence=block.confidence,
            source=block.source,
            metadata=block.metadata,
            language_metadata=meta
        )
        return enriched

    async def process(self, progress_callback: Optional[Callable[[int, str], None]] = None) -> str:
        """
        Orchestrates language processing over the canonical lesson.json.
        Returns the absolute filepath to the generated lesson_language.json.
        """
        start_time = time.time()
        
        if progress_callback:
            progress_callback(0, "Initializing Language Intelligence Engine.")
        self.logger.info(f"[{self.job_id}] Starting Language Intelligence Engine pipeline.")
            
        if not os.path.exists(self.input_file):
            self.logger.error(f"[{self.job_id}] Input file not found: {self.input_file}")
            raise FileNotFoundError(f"Input file not found at {self.input_file}")
            
        with open(self.input_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            doc_result = DocumentIntelligenceResult(**raw_data)
            
        total_blocks = len(doc_result.blocks)
        self.logger.info(f"[{self.job_id}] Loaded lesson.json with {total_blocks} blocks.")
        enriched_blocks = []
        
        # Process blocks concurrently for performance
        tasks = []
        for block in doc_result.blocks:
            tasks.append(self._process_block(block))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for idx, res in enumerate(results):
            if isinstance(res, Exception):
                # Fallback to deterministic block reconstruction if an unhandled error occurred
                block = doc_result.blocks[idx]
                self.logger.warning(f"[{self.job_id}] Unhandled exception in block {block.block_id}: {res}. Falling back to deterministic.")
                
                # Check if processor has deterministic fallback before attempting fallback
                fallback_processor = getattr(self.processor, "deterministic_fallback", None)
                if fallback_processor:
                    meta = await fallback_processor.process(original_text=block.text)
                else:
                    # In case active processor has no fallback, use inline default
                    from services.language_intelligence.processors.deterministic import DeterministicProcessor
                    meta = await DeterministicProcessor().process(original_text=block.text)
                    
                enriched = EnrichedDocumentBlock(
                    **block.model_dump(),
                    language_metadata=meta
                )
                enriched_blocks.append(enriched)
                doc_result.metrics.recoverable_errors.append(f"Block {block.block_id} failed semantic processing: {res}")
            else:
                enriched_blocks.append(res)
                
        if progress_callback:
            progress_callback(90, "Semantic processing completed.")
        self.logger.info(f"[{self.job_id}] Processed {len(enriched_blocks)} blocks.")
            
        end_time = time.time()
        
        # Update metrics
        doc_result.metrics.execution_time += (end_time - start_time)
        doc_result.metrics.progress = 100.0
        
        final_result = LanguageIntelligenceResult(
            metadata=doc_result.metadata,
            blocks=enriched_blocks,
            assets=doc_result.assets,
            metrics=doc_result.metrics
        )
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(final_result.model_dump_json(indent=2))
            
        if progress_callback:
            progress_callback(100, "Language Intelligence Engine finished.")
            
        return self.output_file
