from services.presentation.schemas import PresentationSessionModel
from services.presentation.optimizer.cleanup import ResourcesCleanup
from services.presentation.optimizer.compression import PackageCompression
from typing import Dict, Any

class PresentationOptimizer:
    def __init__(self) -> None:
        pass

    def optimize(self, session: PresentationSessionModel) -> Dict[str, Any]:
        dups = ResourcesCleanup.cleanup_duplicate_assets(session)
        unused = ResourcesCleanup.cleanup_unused_resources(session)
        ratio = PackageCompression.compress_package(session)
        meta = PackageCompression.compress_metadata(session)
        
        return {
            "duplicate_assets_removed": dups,
            "unused_resources_removed": unused,
            "package_compression_ratio": ratio,
            "metadata_keys_compressed": meta
        }
