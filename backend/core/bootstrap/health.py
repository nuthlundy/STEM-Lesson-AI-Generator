from core.validation.validator import SystemValidator

class PlatformHealthCheck:
    @staticmethod
    def run_preflight(workspace_root: str = None) -> bool:
        try:
            SystemValidator.validate_platform(workspace_root)
            return True
        except Exception:
            return False
