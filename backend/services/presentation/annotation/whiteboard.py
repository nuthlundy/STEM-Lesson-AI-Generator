from typing import List, Dict, Any

class Whiteboard:
    def __init__(self) -> None:
        self.actions: List[Dict[str, Any]] = []

    def create(self) -> None:
        self.actions.append({"action": "create"})

    def clear(self) -> None:
        self.actions.clear()
        self.actions.append({"action": "clear"})

    def save(self) -> List[Dict[str, Any]]:
        return list(self.actions)
