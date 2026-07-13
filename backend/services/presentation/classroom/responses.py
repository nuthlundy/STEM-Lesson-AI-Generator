from typing import Dict, Any, List

class StudentResponses:
    def __init__(self) -> None:
        self._participation: Dict[str, int] = {}

    def track_response(self, student_id: str) -> None:
        self._participation[student_id] = self._participation.get(student_id, 0) + 1

    def get_participation_count(self, student_id: str) -> int:
        return self._participation.get(student_id, 0)
