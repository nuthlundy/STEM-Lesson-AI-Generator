import asyncio
from core.logger import get_logger
from services.document_intelligence.engine import DocumentIntelligenceEngine

logger = get_logger("stem_ai.workers.pdf")

async def process_pdf_job(job_id: str, file_path: str, original_filename: str):
    """
    Background worker for processing uploaded PDF documents.
    Triggers the Document Intelligence Engine and simulates subsequent engines.
    """
    logger.info(f"[Job: {job_id}] Started processing: {original_filename}")
    
    # 1. Document Intelligence Engine (Phase 3)
    logger.info(f"[Job: {job_id}] Phase 3: Document Intelligence Engine (DIE) starting...")
    try:
        def progress_callback(percent: int, message: str):
            logger.info(f"[Job: {job_id}] [Progress {percent}%] {message}")

        engine = DocumentIntelligenceEngine(job_id, file_path, original_filename)
        lesson_json_path = await engine.process(progress_callback=progress_callback)
        logger.info(f"[Job: {job_id}] Phase 3 complete. lesson.json generated at: {lesson_json_path}")
    except Exception as e:
        logger.error(f"[Job: {job_id}] Phase 3 failed: {e}")
        return
    
    # 2. Language Intelligence Engine (Phase 4)
    logger.info(f"[Job: {job_id}] Phase 4: Language Intelligence Engine (LIE) starting...")
    try:
        from services.language_intelligence.engine import LanguageIntelligenceEngine
        lie_engine = LanguageIntelligenceEngine(job_id)
        lesson_language_path = await lie_engine.process(progress_callback=progress_callback)
        logger.info(f"[Job: {job_id}] Phase 4 complete. lesson_language.json generated at: {lesson_language_path}")
    except Exception as e:
        logger.error(f"[Job: {job_id}] Phase 4 failed: {e}")
        return    
    # 3. Subject Intelligence Engine (Phase 5 - simulated stub)
    logger.info(f"[Job: {job_id}] Phase 5: Subject Intelligence Engine (SIE)...")
    await asyncio.sleep(2)
    
    # 4. Lesson Planning Engine (Phase 6 - simulated stub)
    logger.info(f"[Job: {job_id}] Phase 6: Lesson Planning Engine (LPE)...")
    await asyncio.sleep(2)
    
    logger.info(f"[Job: {job_id}] Processing complete for: {original_filename}")
    
    # Future: Update database with 'completed' status and lesson.json
