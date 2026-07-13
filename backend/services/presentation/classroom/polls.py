from typing import Dict, Any, List

class ClassroomPolls:
    def __init__(self) -> None:
        self._polls: Dict[str, Dict[str, Any]] = {}

    def create_poll(self, poll_id: str, question: str, options: List[str]) -> None:
        self._polls[poll_id] = {
            "question": question,
            "options": options,
            "responses": [],
            "active": True
        }

    def collect_response(self, poll_id: str, student_id: str, option_index: int) -> None:
        if poll_id in self._polls and self._polls[poll_id]["active"]:
            self._polls[poll_id]["responses"].append({
                "student_id": student_id,
                "option_index": option_index
            })

    def summarize(self, poll_id: str) -> Dict[int, int]:
        if poll_id not in self._polls:
            return {}
        summary: Dict[int, int] = {}
        for resp in self._polls[poll_id]["responses"]:
            opt = resp["option_index"]
            summary[opt] = summary.get(opt, 0) + 1
        return summary
