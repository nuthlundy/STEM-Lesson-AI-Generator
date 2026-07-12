from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePlugin(ABC):
    """Abstract base class representing a platform plugin."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Lifecycle hook called when the plugin is loaded and initialized."""
        pass

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """Executes the plugin core logic with a given runtime context."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Lifecycle hook called when the plugin is unloaded or shut down."""
        pass

    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """Returns metadata about the plugin (e.g. name, type, version, description)."""
        pass
