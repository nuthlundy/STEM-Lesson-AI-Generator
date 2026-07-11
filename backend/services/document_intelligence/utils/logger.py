import logging
from typing import Optional, List
from core.logger import get_logger

class DIELogger:
    def __init__(self, job_id: str):
        self.job_id = job_id
        # Use the standard logger configured in core.logger
        self.logger = get_logger("stem_ai")
        self.warnings: List[str] = []
        self.recoverable_errors: List[str] = []
        self.fatal_errors: List[str] = []

    def _format_msg(self, msg: str, page: Optional[int]) -> str:
        prefix = f"[Job: {self.job_id}]"
        if page is not None:
            prefix += f" [Page: {page}]"
        return f"{prefix} {msg}"

    def info(self, msg: str, page: Optional[int] = None) -> None:
        self.logger.info(self._format_msg(msg, page))

    def debug(self, msg: str, page: Optional[int] = None) -> None:
        # standard debug log
        self.logger.debug(self._format_msg(msg, page))

    def warning(self, msg: str, page: Optional[int] = None) -> None:
        formatted = self._format_msg(msg, page)
        self.logger.warning(formatted)
        self.warnings.append(formatted)

    def recoverable_error(self, msg: str, page: Optional[int] = None) -> None:
        formatted = self._format_msg(f"[Recoverable] {msg}", page)
        self.logger.error(formatted)
        self.recoverable_errors.append(formatted)

    def fatal_error(self, msg: str, page: Optional[int] = None) -> None:
        formatted = self._format_msg(f"[Fatal] {msg}", page)
        self.logger.critical(formatted)
        self.fatal_errors.append(formatted)
