import time
import os
from typing import Dict, Any
from core.bootstrap.loader import PlatformLoader
from core.bootstrap.initializer import PlatformInitializer
from core.bootstrap.health import PlatformHealthCheck
from core.validation.exceptions import ValidationError

STARTUP_DURATION = 0.0
MEMORY_STATS = {"rss_mb": 0.0}

class PlatformBootstrap:
    @staticmethod
    def bootstrap(workspace_root: str = None, config_path: str = None) -> Dict[str, Any]:
        global STARTUP_DURATION, MEMORY_STATS
        start_time = time.time()
        PlatformLoader.load_config(config_path)
        success = PlatformHealthCheck.run_preflight(workspace_root)
        if not success:
            raise ValidationError("Platform pre-flight validation failed during bootstrapping.")
        result = PlatformInitializer.initialize()
        
        STARTUP_DURATION = round(time.time() - start_time, 4)

        
        # collect memory statistics safely
        try:
            import psutil
            process = psutil.Process(os.getpid())
            MEMORY_STATS["rss_mb"] = round(process.memory_info().rss / (1024 * 1024), 2)
        except Exception:
            pass
            
        PlatformBootstrap._cached_result = result
        return result

