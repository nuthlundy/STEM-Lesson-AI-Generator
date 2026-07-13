from abc import ABC, abstractmethod
from typing import Dict, Any

class ExporterInterface(ABC):
    @abstractmethod
    def export(self, session_path: str, output_path: str) -> None:
        pass

    @abstractmethod
    def validate(self, output_path: str) -> bool:
        pass

    @abstractmethod
    def metadata(self, output_path: str) -> Dict[str, Any]:
        pass
