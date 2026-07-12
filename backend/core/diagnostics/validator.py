from typing import Dict, Any, List
from core.artifacts.registry import ArtifactRegistry
from core.config.registry import ConfigRegistry

class DiagnosticsValidator:
    @staticmethod
    def validate_artifacts(registry: ArtifactRegistry) -> Dict[str, Any]:
        issues = []
        for artifact in registry.list():
            name = artifact.artifact_id
            try:
                registry.validate(name)
            except Exception as e:
                issues.append({"artifact": name, "error": str(e)})
        return {
            "status": "Healthy" if not issues else "Critical",
            "issues": issues
        }

    @staticmethod
    def validate_config(registry: ConfigRegistry) -> Dict[str, Any]:
        issues = []
        for provider in registry.list_providers():
            meta = provider.model_dump()
            if not meta.get("model_name"):
                issues.append({"provider": meta.get("provider_type"), "error": "Missing model_name configuration."})
        return {
            "status": "Healthy" if not issues else "Critical",
            "issues": issues
        }
