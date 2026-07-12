import os
import sys
import threading
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from core.logging.formatter import BaseFormatter, JsonFormatter

class BaseHandler(ABC):
    def __init__(self, formatter: BaseFormatter = None):
        self.formatter = formatter if formatter else JsonFormatter()
        self._lock = threading.Lock()

    @abstractmethod
    def emit(self, level: str, message: str, extra: Dict[str, Any] = None) -> None:
        pass

class ConsoleHandler(BaseHandler):
    def emit(self, level: str, message: str, extra: Dict[str, Any] = None) -> None:
        formatted = self.formatter.format(level, message, extra)
        with self._lock:
            sys.stdout.write(formatted + "\n")
            sys.stdout.flush()

class FileHandler(BaseHandler):
    def __init__(self, file_path: str, formatter: BaseFormatter = None):
        super().__init__(formatter)
        self.file_path = file_path
        dir_name = os.path.dirname(self.file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

    def emit(self, level: str, message: str, extra: Dict[str, Any] = None) -> None:
        formatted = self.formatter.format(level, message, extra)
        with self._lock:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")

class NullHandler(BaseHandler):
    def emit(self, level: str, message: str, extra: Dict[str, Any] = None) -> None:
        pass
