from typing import Set, List

class AttendanceTracker:
    def __init__(self) -> None:
        self._present: Set[str] = set()

    def mark_present(self, student_id: str) -> None:
        self._present.add(student_id)

    def get_present_students(self) -> List[str]:
        return sorted(list(self._present))
