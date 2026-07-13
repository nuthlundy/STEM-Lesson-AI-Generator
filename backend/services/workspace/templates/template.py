from pydantic import BaseModel
from typing import List

class LessonTemplate(BaseModel):
    template_id: str
    template_name: str
    category: str
    description: str
    version: str = "1.0.0"
    supported_curriculum: str = "NGSS"
    supported_grades: List[str] = []
    created_timestamp: float
