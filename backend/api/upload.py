import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from core.logger import get_logger
from config.settings import settings
from workers.pdf_worker import process_pdf_job

router = APIRouter(tags=["Upload"])
logger = get_logger("stem_ai.api.upload")

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    job_id = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{job_id}_{file.filename}")
    
    logger.info(f"Received file: {file.filename} -> Job ID: {job_id}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")
        
    # Queue background processing
    background_tasks.add_task(process_pdf_job, job_id, file_path, file.filename)
    
    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Document uploaded successfully and queued for processing."
    }
