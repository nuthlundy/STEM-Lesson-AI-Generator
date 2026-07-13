from typing import List, Dict, Any

class ClassroomDiscussions:
    def __init__(self) -> None:
        self._discussions: Dict[str, Dict[str, Any]] = {}

    def add_discussion(self, discussion_id: str, prompt: str, follow_ups: List[str]) -> None:
        self._discussions[discussion_id] = {
            "prompt": prompt,
            "follow_ups": follow_ups
        }

    def get_discussion(self, discussion_id: str) -> Dict[str, Any]:
        return self._discussions.get(discussion_id, {})
