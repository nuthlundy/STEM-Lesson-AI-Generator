from pydantic import BaseModel, Field

class PresentationConfig(BaseModel):
    duration_seconds: int = Field(default=3600, ge=300, le=28800)
    view_mode: str = "standard"
    enable_presenter_view: bool = True
