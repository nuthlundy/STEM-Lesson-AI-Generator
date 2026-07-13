from typing import List, Set

class PresentationTracker:
    def __init__(self) -> None:
        self._completed_slides: Set[int] = set()
        self._actual_elapsed_time = 0.0

    def mark_slide_completed(self, slide_index: int) -> None:
        self._completed_slides.add(slide_index)

    def get_completed_slides(self) -> List[int]:
        return sorted(list(self._completed_slides))

    def set_actual_elapsed_time(self, seconds: float) -> None:
        self._actual_elapsed_time = seconds

    def get_actual_elapsed_time(self) -> float:
        return self._actual_elapsed_time
