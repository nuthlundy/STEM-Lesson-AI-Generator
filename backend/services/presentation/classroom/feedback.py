from typing import List, Dict, Any

class ClassroomFeedback:
    def __init__(self) -> None:
        self._feedback_list: List[Dict[str, Any]] = []

    def collect_feedback(self, student_id: str, rating: int, comment: str = "") -> None:
        self._feedback_list.append({
            "student_id": student_id,
            "rating": rating,
            "comment": comment
        })

    def summarize_feedback(self) -> Dict[str, Any]:
        if not self._feedback_list:
            return {"average_rating": 0.0, "total_responses": 0}
        ratings = [f["rating"] for f in self._feedback_list]
        return {
            "average_rating": sum(ratings) / len(ratings),
            "total_responses": len(self._feedback_list)
        }
