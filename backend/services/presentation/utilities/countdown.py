class Countdown:
    def __init__(self, limit_seconds: int = 60) -> None:
        self.limit_seconds = limit_seconds
        self._remaining = limit_seconds

    def tick(self, seconds: int = 1) -> int:
        self._remaining = max(0, self._remaining - seconds)
        return self._remaining

    def get_remaining(self) -> int:
        return self._remaining
