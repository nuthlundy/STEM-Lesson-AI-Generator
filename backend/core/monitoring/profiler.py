import os
import time
from typing import Dict, Any, Optional

try:
    import psutil
    def get_current_memory_bytes() -> int:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss
except ImportError:
    def get_current_memory_bytes() -> int:
        return 1024 * 1024 * 50

class Profiler:
    """Context manager or utility to track execution durations and memory spikes."""
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0
        self.start_memory = 0
        self.end_memory = 0
        self.peak_memory = 0

    def __enter__(self):
        self.start_time = time.time()
        self.start_memory = get_current_memory_bytes()
        self.peak_memory = self.start_memory
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.end_memory = get_current_memory_bytes()
        if self.end_memory > self.peak_memory:
            self.peak_memory = self.end_memory

    @property
    def duration(self) -> float:
        if self.start_time > 0:
            end = self.end_time if self.end_time > 0 else time.time()
            return round(end - self.start_time, 4)
        return 0.0
