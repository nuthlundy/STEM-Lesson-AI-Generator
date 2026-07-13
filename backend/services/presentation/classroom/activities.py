from typing import Dict, Any, List

class ClassroomActivities:
    def __init__(self) -> None:
        self._activities: Dict[str, Dict[str, Any]] = {}

    def create_activity(self, activity_id: str, name: str, activity_type: str = "think-pair-share") -> None:
        self._activities[activity_id] = {
            "name": name,
            "type": activity_type,
            "status": "created"
        }

    def get_activity(self, activity_id: str) -> Dict[str, Any]:
        return self._activities.get(activity_id, {})
