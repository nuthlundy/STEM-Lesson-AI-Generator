from typing import Dict, List
from core.plugins.plugin import BasePlugin
from core.plugins.exceptions import (
    DuplicatePluginError,
    PluginNotFoundError,
    InvalidPluginError
)

class PluginRegistry:
    """Manages memory registration, lookup, and validation of platform plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}

    def register_plugin(self, plugin: BasePlugin) -> None:
        self.validate_plugin(plugin)
        meta = plugin.metadata()
        plugin_id = meta["id"]
        
        if plugin_id in self._plugins:
            raise DuplicatePluginError(f"Plugin '{plugin_id}' is already registered.")
            
        self._plugins[plugin_id] = plugin

    def unregister_plugin(self, plugin_id: str) -> None:
        if plugin_id in self._plugins:
            del self._plugins[plugin_id]

    def get_plugin(self, plugin_id: str) -> BasePlugin:
        if plugin_id not in self._plugins:
            raise PluginNotFoundError(f"Plugin '{plugin_id}' not found in registry.")
        return self._plugins[plugin_id]

    def list_plugins(self) -> List[BasePlugin]:
        return list(self._plugins.values())

    def validate_plugin(self, plugin: BasePlugin) -> None:
        if not isinstance(plugin, BasePlugin):
            raise InvalidPluginError("Plugin must inherit from BasePlugin.")
            
        try:
            meta = plugin.metadata()
        except Exception as e:
            raise InvalidPluginError(f"Plugin metadata query failed: {e}")
            
        if not isinstance(meta, dict):
            raise InvalidPluginError("Plugin metadata must return a dictionary.")
            
        for key in ("id", "name", "version", "type"):
            if key not in meta or not str(meta[key]).strip():
                raise InvalidPluginError(f"Plugin metadata missing required field: '{key}'")
