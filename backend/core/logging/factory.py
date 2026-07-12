import threading
from typing import Dict
from core.logging.logger import Logger

_loggers: Dict[str, Logger] = {}
_loggers_lock = threading.Lock()

class LoggerFactory:
    @staticmethod
    def get_logger(name: str, level: str = "INFO") -> Logger:
        with _loggers_lock:
            if name not in _loggers:
                _loggers[name] = Logger(name, level)
            return _loggers[name]

    @staticmethod
    def clear_loggers() -> None:
        with _loggers_lock:
            _loggers.clear()
