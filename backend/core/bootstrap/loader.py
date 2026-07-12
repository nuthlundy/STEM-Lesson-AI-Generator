from core.config.loader import ConfigLoader
from core.config.registry import get_canonical_config_registry

class PlatformLoader:
    @staticmethod
    def load_config(config_path: str = None) -> None:
        reg = get_canonical_config_registry()
        settings = ConfigLoader.load(config_path)
        reg.update_settings(settings)
