import threading
import time
from typing import Callable

class AutosaveScheduler:
    def __init__(self, interval: float = 60.0, callback: Callable[[], None] = None) -> None:
        self.interval = interval
        self.callback = callback
        self.running = False
        self._thread = None

    def start(self) -> None:
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def stop(self) -> None:
        self.running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _run(self) -> None:
        while self.running:
            time.sleep(self.interval)
            if self.running and self.callback:
                try:
                    self.callback()
                except Exception:
                    pass
