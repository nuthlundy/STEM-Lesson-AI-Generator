from services.presentation.schemas import PresentationSessionModel

class PackageCompression:
    @staticmethod
    def compress_package(session: PresentationSessionModel) -> float:
        return 1.0

    @staticmethod
    def compress_metadata(session: PresentationSessionModel) -> int:
        return 0
