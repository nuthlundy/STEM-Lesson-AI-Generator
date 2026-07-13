from services.presentation.schemas import PresentationSessionModel

class ResourcesCleanup:
    @staticmethod
    def cleanup_duplicate_assets(session: PresentationSessionModel) -> int:
        return 0

    @staticmethod
    def cleanup_unused_resources(session: PresentationSessionModel) -> int:
        return 0
