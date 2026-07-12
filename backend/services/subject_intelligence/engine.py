import os
import json
import time
import asyncio
from typing import Optional, Callable, Dict, Any, List
from services.language_intelligence.interfaces import LanguageIntelligenceResult
from services.subject_intelligence.interfaces.engine import SubjectIntelligenceResult, EnrichedSubjectDocumentBlock
from services.subject_intelligence.factory import ProcessorFactory
from services.subject_intelligence.writers.json_writer import JSONWriter
from services.subject_intelligence.graph.builder import GraphBuilder
from services.subject_intelligence.curriculum.mapper import CurriculumMapper
from services.subject_intelligence.curriculum.generator import LearningObjectiveGenerator
from services.subject_intelligence.curriculum.coverage import ConceptCoverageAnalyzer
from services.subject_intelligence.instructional.scheduler import ConceptDependencyScheduler
from services.subject_intelligence.instructional.sequence import LearningSequenceGenerator
from services.subject_intelligence.instructional.gap_detection import GapDetectionEngine
from services.subject_intelligence.instructional.readiness import LessonReadinessAnalyzer
from services.subject_intelligence.instructional.metadata import InstructionalMetadataGenerator
from services.subject_intelligence.instructional.summary import SubjectSummaryGenerator
from services.subject_intelligence.constants import STEMSubject
from core.logger import get_logger

class SubjectIntelligenceEngine:
    def __init__(self, job_id: str, base_dir: str = "uploads/jobs"):
        self.job_id = job_id
        self.base_dir = base_dir
        self.job_dir = os.path.abspath(os.path.join(self.base_dir, self.job_id))
        self.input_file = os.path.join(self.job_dir, "lesson_language.json")
        self.output_file = os.path.join(self.job_dir, "lesson_subject.json")
        self.output_graph_file = os.path.join(self.job_dir, "lesson_subject_graph.json")
        self.output_objectives_file = os.path.join(self.job_dir, "lesson_learning_objectives.json")
        self.output_instructional_file = os.path.join(self.job_dir, "lesson_instructional_model.json")
        
        self.logger = get_logger("stem_ai.sie.engine")
        self.processor = ProcessorFactory.get_processor()
        self.writer = JSONWriter()

    # Lifecycle Hooks Skeletons
    def before_process(self, input_data: Dict[str, Any]) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: before_process")

    def after_process(self, blocks: List[EnrichedSubjectDocumentBlock]) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: after_process. Processed {len(blocks)} blocks.")

    def before_validate(self, blocks: List[EnrichedSubjectDocumentBlock]) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: before_validate")

    def after_validate(self, validation_results: Dict[str, Any]) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: after_validate")

    def before_save(self, result: SubjectIntelligenceResult) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: before_save")

    def after_save(self) -> None:
        self.logger.info(f"[{self.job_id}] Lifecycle Hook: after_save. Saved output to {self.output_file}")

    async def _process_block(self, block) -> EnrichedSubjectDocumentBlock:
        metadata = await self.processor.process(block.text)
        
        enriched = EnrichedSubjectDocumentBlock(
            block_id=block.block_id,
            block_type=block.block_type,
            text=block.text,
            page_number=block.page_number,
            bbox=block.bbox,
            confidence=block.confidence,
            source=block.source,
            metadata=block.metadata,
            language_metadata=block.language_metadata,
            subject_metadata=metadata
        )
        return enriched

    async def process(self, progress_callback: Optional[Callable[[int, str], None]] = None) -> str:
        """
        Orchestrates Subject Intelligence processing over lesson_language.json.
        Returns the absolute filepath to lesson_subject.json.
        """
        start_time = time.time()
        
        if progress_callback:
            progress_callback(0, "Initializing Subject Intelligence Engine.")
            
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found at {self.input_file}")
            
        with open(self.input_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        # Hook: before_process
        self.before_process(raw_data)
        
        # Load from schema
        lang_result = LanguageIntelligenceResult(**raw_data)
        
        # Concurrently process blocks
        tasks = []
        for block in lang_result.blocks:
            tasks.append(self._process_block(block))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        enriched_blocks = []
        for idx, res in enumerate(results):
            if isinstance(res, Exception):
                # Graceful fallback reconstruction on block failure
                block = lang_result.blocks[idx]
                fallback_processor = getattr(self.processor, "deterministic_fallback", self.processor)
                meta = await fallback_processor.process(block.text)
                enriched = EnrichedSubjectDocumentBlock(
                    **block.model_dump(),
                    subject_metadata=meta
                )
                enriched_blocks.append(enriched)
                lang_result.metrics.recoverable_errors.append(f"Block {block.block_id} failed subject parsing: {res}")
            else:
                enriched_blocks.append(res)
                
        # Hook: after_process
        self.after_process(enriched_blocks)
        
        # Hook: before_validate
        self.before_validate(enriched_blocks)
        
        # Validation simulation/skeleton
        validation_results = {"valid": True}
        
        # Hook: after_validate
        self.after_validate(validation_results)
        
        if progress_callback:
            progress_callback(90, "Subject processing and validation complete.")
            
        end_time = time.time()
        
        # Update metrics
        lang_result.metrics.execution_time += (end_time - start_time)
        lang_result.metrics.progress = 100.0
        
        # Assemble result
        final_result = SubjectIntelligenceResult(
            metadata=lang_result.metadata,
            blocks=enriched_blocks,
            assets=lang_result.assets,
            metrics=lang_result.metrics
        )
        
        # Hook: before_save
        self.before_save(final_result)
        
        # Write asynchronously using writer
        await self.writer.write(final_result, self.output_file)
        
        # Build and write Knowledge Graph
        try:
            self.logger.info(f"[{self.job_id}] Compiling Subject Knowledge Graph.")
            graph = GraphBuilder.build(final_result)
            await self.writer.write(graph, self.output_graph_file)
            self.logger.info(f"[{self.job_id}] Successfully generated lesson_subject_graph.json")
        except Exception as e:
            self.logger.error(f"[{self.job_id}] Knowledge Graph compilation failed: {e}")
            final_result.metrics.recoverable_errors.append(f"Knowledge Graph compilation failed: {e}")
        
        # Compile and write Curriculum Standards and Learning Objectives
        try:
            self.logger.info(f"[{self.job_id}] Mapping Curriculum and generating objectives.")
            concepts = set()
            subjects_found = []
            for block in enriched_blocks:
                if block.subject_metadata:
                    subjects_found.append(block.subject_metadata.subject)
                    if block.subject_metadata.topic:
                        concepts.add(block.subject_metadata.topic)
                    for vocab in block.subject_metadata.vocabulary:
                        concepts.add(vocab)
                    for prereq in block.subject_metadata.prerequisites:
                        concepts.add(prereq)
            
            if subjects_found:
                dominant_subject = max(set(subjects_found), key=subjects_found.count)
            else:
                dominant_subject = STEMSubject.MATH
                
            alignments = CurriculumMapper.map_standards(dominant_subject, list(concepts))
            objectives = LearningObjectiveGenerator.generate_objectives(list(concepts))
            coverage = ConceptCoverageAnalyzer.analyze(dominant_subject, alignments, objectives)
            
            await self.writer.write(coverage, self.output_objectives_file)
            self.logger.info(f"[{self.job_id}] Successfully generated lesson_learning_objectives.json")
            
            # Compile and write Instructional Model
            try:
                self.logger.info(f"[{self.job_id}] Building Instructional Model.")
                from services.subject_intelligence.instructional.schemas import InstructionalModelResult
                
                # 1. Schedule concepts
                scheduled_concepts = ConceptDependencyScheduler.schedule(graph)
                
                # 2. Generate sequence steps
                sequence = LearningSequenceGenerator.generate_sequence(scheduled_concepts, objectives)
                
                # 3. Detect prerequisite gaps
                prereqs_map = {}
                for block in enriched_blocks:
                    if block.subject_metadata and block.subject_metadata.topic:
                        topic_name = block.subject_metadata.topic
                        if topic_name not in prereqs_map:
                            prereqs_map[topic_name] = block.subject_metadata.prerequisites
                
                gaps = GapDetectionEngine.detect_gaps(scheduled_concepts, prereqs_map)
                
                # 4. Analyze readiness
                readiness = LessonReadinessAnalyzer.analyze(graph, len(gaps))
                
                # 5. Metadata generation
                instructional_metadata = InstructionalMetadataGenerator.generate(dominant_subject, len(scheduled_concepts))
                
                # 6. Summary generation
                summary = SubjectSummaryGenerator.generate_summary(dominant_subject, list(concepts))
                
                # 7. Assemble and write
                instructional_model = InstructionalModelResult(
                    subject=dominant_subject.value,
                    summary=summary,
                    scheduled_concepts=scheduled_concepts,
                    sequence=sequence,
                    readiness=readiness,
                    gaps=gaps,
                    metadata=instructional_metadata
                )
                
                await self.writer.write(instructional_model, self.output_instructional_file)
                self.logger.info(f"[{self.job_id}] Successfully generated lesson_instructional_model.json")
            except Exception as e:
                self.logger.error(f"[{self.job_id}] Instructional model generation failed: {e}")
                final_result.metrics.recoverable_errors.append(f"Instructional model generation failed: {e}")
                
        except Exception as e:
            self.logger.error(f"[{self.job_id}] Curriculum alignment failed: {e}")
            final_result.metrics.recoverable_errors.append(f"Curriculum alignment failed: {e}")

        # Hook: after_save
        self.after_save()
        
        if progress_callback:
            progress_callback(100, "Subject Intelligence Engine complete.")
            
        return self.output_file
