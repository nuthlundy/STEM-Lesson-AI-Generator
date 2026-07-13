class BreakReminder:
    def __init__(self, interval_seconds: int = 1800) -> None:
        self.interval_seconds = interval_seconds

    def should_break(self, elapsed: float) -> bool:
        return elapsed >= self.interval_seconds
