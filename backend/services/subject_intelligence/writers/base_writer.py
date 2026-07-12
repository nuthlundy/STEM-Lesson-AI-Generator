from abc import ABC, abstractmethod
from typing import Any

class BaseWriter(ABC):
    """Abstract base class for serialization writers."""
    @abstractmethod
    async def write(self, data: Any, filepath: str) -> None:
        """Write data to the specified path asynchronously."""
        pass
