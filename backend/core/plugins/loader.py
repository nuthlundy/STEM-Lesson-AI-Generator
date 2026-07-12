from typing import Type
from core.plugins.plugin import BasePlugin

class PluginLoader:
    """Loads and instantiates plugin classes."""
    @staticmethod
    def load_plugin(plugin_class: Type[BasePlugin]) -> BasePlugin:
        return plugin_class()
