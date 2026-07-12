from pydantic import BaseModel, Field
from typing import List

class RenderingConfig(BaseModel):
    theme: str = "modern"
    default_format: str = "html"
    supported_formats: List[str] = Field(default_factory=lambda: ["html", "pdf", "pptx"])
