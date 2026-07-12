from typing import Dict, Any, List
from core.plugins.registry import PluginRegistry
from core.plugins.plugin import BasePlugin

class PluginManager:
    """Manages the lifecycle (initialization, execution, shutdown) of platform plugins."""
    
    def __init__(self, registry: PluginRegistry = None):
        self.registry = registry if registry else PluginRegistry()

    def initialize_all(self) -> None:
        """Initializes all registered plugins."""
        for plugin in self.registry.list_plugins():
            plugin.initialize()

    def execute_plugin(self, plugin_id: str, context: Dict[str, Any]) -> Any:
        """Executes a registered plugin by ID with a given context."""
        plugin = self.registry.get_plugin(plugin_id)
        return plugin.execute(context)

    def shutdown_all(self) -> None:
        """Gracefully shuts down all registered plugins."""
        for plugin in self.registry.list_plugins():
            plugin.shutdown()
