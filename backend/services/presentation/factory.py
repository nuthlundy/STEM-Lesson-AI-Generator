from services.presentation.config import PresentationConfig

class PresentationPresenterFactory:
    @staticmethod
    def create_config(duration: int = 3600, view_mode: str = "standard") -> PresentationConfig:
        return PresentationConfig(duration_seconds=duration, view_mode=view_mode)
