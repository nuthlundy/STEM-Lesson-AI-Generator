import threading
from typing import List, Dict, Any, Optional
from core.logging.handlers import BaseHandler
from core.logging.exceptions import InvalidLogLevelError, InvalidHandlerError

LOG_LEVEL_VALUES = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50
}

class Logger:
    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.set_level(level)
        self.handlers: List[BaseHandler] = []
        self._lock = threading.Lock()

    def set_level(self, level: str) -> None:
        upper_level = level.upper()
        if upper_level not in LOG_LEVEL_VALUES:
            raise InvalidLogLevelError(f"Invalid log level: {level}")
        self.level = upper_level
        self._level_val = LOG_LEVEL_VALUES[upper_level]

    def add_handler(self, handler: BaseHandler) -> None:
        with self._lock:
            for existing in self.handlers:
                if type(existing) == type(handler):
                    if hasattr(existing, "file_path") and hasattr(handler, "file_path"):
                        if getattr(existing, "file_path") == getattr(handler, "file_path"):
                            raise InvalidHandlerError("Duplicate FileHandler registered.")
                    elif not hasattr(existing, "file_path") and not hasattr(handler, "file_path"):
                        raise InvalidHandlerError(f"Duplicate handler of type {type(handler).__name__} registered.")
            self.handlers.append(handler)

    def remove_handler(self, handler: BaseHandler) -> None:
        with self._lock:
            if handler in self.handlers:
                self.handlers.remove(handler)

    def _log(self, level: str, message: str, extra: Dict[str, Any] = None) -> None:
        level_val = LOG_LEVEL_VALUES[level]
        if level_val >= self._level_val:
            handlers_copy = []
            with self._lock:
                handlers_copy = list(self.handlers)
            for handler in handlers_copy:
                handler.emit(level, message, extra)

    def debug(self, message: str, extra: Dict[str, Any] = None) -> None:
        self._log("DEBUG", message, extra)

    def info(self, message: str, extra: Dict[str, Any] = None) -> None:
        self._log("INFO", message, extra)

    def warning(self, message: str, extra: Dict[str, Any] = None) -> None:
        self._log("WARNING", message, extra)

    def error(self, message: str, extra: Dict[str, Any] = None) -> None:
        self._log("ERROR", message, extra)

    def critical(self, message: str, extra: Dict[str, Any] = None) -> None:
        self._log("CRITICAL", message, extra)
