from typing import Dict, Any
from core.bootstrap.loader import PlatformLoader
from core.bootstrap.initializer import PlatformInitializer
from core.bootstrap.health import PlatformHealthCheck
from core.validation.exceptions import ValidationError

class PlatformBootstrap:
    @staticmethod
    def bootstrap(workspace_root: str = None, config_path: str = None) -> Dict[str, Any]:
        PlatformLoader.load_config(config_path)
        success = PlatformHealthCheck.run_preflight(workspace_root)
        if not success:
            raise ValidationError("Platform pre-flight validation failed during bootstrapping.")
        return PlatformInitializer.initialize()
