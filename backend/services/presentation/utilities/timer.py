import time

class LessonTimer:
    def __init__(self) -> None:
        self._start = time.time()

    def elapsed_seconds(self) -> float:
        return time.time() - self._start
