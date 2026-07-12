from typing import Dict, Any, List
from core.plugins.registry import PluginRegistry

class PluginInspector:
    @staticmethod
    def inspect_plugins(registry: PluginRegistry) -> Dict[str, Any]:
        results = {
            "total_plugins": 0,
            "broken_plugins": [],
            "status": "Healthy"
        }
        plugins = registry.list_plugins()
        results["total_plugins"] = len(plugins)
        
        for plugin in plugins:
            try:
                meta = plugin.metadata()
                for key in ("id", "name", "version", "type"):
                    if key not in meta or not str(meta[key]).strip():
                        results["broken_plugins"].append({
                            "id": meta.get("id", "unknown"),
                            "reason": f"Missing metadata key: '{key}'"
                        })
                        results["status"] = "Critical"
                        break
            except Exception as e:
                results["broken_plugins"].append({
                    "id": "unknown",
                    "reason": f"Plugin failed metadata inspect: {e}"
                })
                results["status"] = "Critical"
        return results
