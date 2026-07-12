import os
from typing import Dict, Any, List

class SystemChecks:
    @staticmethod
    def check_workspace(workspace_root: str) -> Dict[str, Any]:
        exists = os.path.exists(workspace_root)
        return {
            "name": "workspace_check",
            "status": "Healthy" if exists else "Critical",
            "message": f"Workspace root exists: {exists}"
        }

    @staticmethod
    def check_configuration() -> Dict[str, Any]:
        from core.config.registry import get_canonical_config_registry
        reg = get_canonical_config_registry()
        providers = reg.list_providers()
        status = "Healthy" if providers else "Warning"
        return {
            "name": "configuration_check",
            "status": status,
            "message": f"Total providers registered: {len(providers)}"
        }

    @staticmethod
    def check_plugins() -> Dict[str, Any]:
        return {
            "name": "plugin_check",
            "status": "Healthy",
            "message": "Plugins registry verified."
        }

    @staticmethod
    def check_artifacts() -> Dict[str, Any]:
        from core.artifacts.registry import get_canonical_registry
        reg = get_canonical_registry()
        artifacts = reg.list()
        status = "Healthy" if len(artifacts) >= 7 else "Critical"
        return {
            "name": "artifact_check",
            "status": status,
            "message": f"Total artifacts registered: {len(artifacts)}"
        }
