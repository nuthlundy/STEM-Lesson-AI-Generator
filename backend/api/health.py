from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "STEM Lesson AI Studio Python Backend"}
