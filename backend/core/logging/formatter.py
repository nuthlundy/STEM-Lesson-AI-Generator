import json
import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any
from core.logging.context import get_logging_context

class BaseFormatter(ABC):
    @abstractmethod
    def format(self, level: str, message: str, extra: Dict[str, Any] = None) -> str:
        pass

class JsonFormatter(BaseFormatter):
    def format(self, level: str, message: str, extra: Dict[str, Any] = None) -> str:
        ctx = get_logging_context()
        log_record = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "level": level,
            "message": message,
            "context": ctx
        }
        if extra:
            log_record["extra"] = extra
        return json.dumps(log_record)

class ConsoleFormatter(BaseFormatter):
    def format(self, level: str, message: str, extra: Dict[str, Any] = None) -> str:
        ctx = get_logging_context()
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        ctx_str = f" [Correlation: {ctx.get('correlation_id')}]"
        if ctx.get('stage_id'):
            ctx_str += f" [Stage: {ctx.get('stage_id')}]"
        extra_str = f" | Extra: {extra}" if extra else ""
        return f"[{timestamp}] [{level}] {message}{ctx_str}{extra_str}"
