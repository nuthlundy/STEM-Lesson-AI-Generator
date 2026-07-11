import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.health import router as health_router
from api.upload import router as upload_router
from core.logger import setup_logger

# Initialize logging
setup_logger()

app = FastAPI(
    title="STEM Lesson AI Studio - Document Intelligence API",
    version="1.0.0",
    description="Python backend for processing STEM educational documents."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
