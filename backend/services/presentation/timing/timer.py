import time
from typing import Optional

class PresentationTimer:
    def __init__(self) -> None:
        self._start_time: Optional[float] = None
        self._elapsed_paused: float = 0.0
        self._paused_time: Optional[float] = None
        self._active = False

    def start(self) -> None:
        if not self._active:
            self._start_time = time.time()
            self._elapsed_paused = 0.0
            self._paused_time = None
            self._active = True

    def pause(self) -> None:
        if self._active and self._paused_time is None:
            self._paused_time = time.time()

    def resume(self) -> None:
        if self._active and self._paused_time is not None:
            self._elapsed_paused += time.time() - self._paused_time
            self._paused_time = None

    def stop(self) -> None:
        self._active = False
        self._start_time = None
        self._paused_time = None

    def get_elapsed_seconds(self) -> float:
        if not self._active or self._start_time is None:
            return 0.0
        if self._paused_time is not None:
            return self._paused_time - self._start_time - self._elapsed_paused
        return time.time() - self._start_time - self._elapsed_paused
