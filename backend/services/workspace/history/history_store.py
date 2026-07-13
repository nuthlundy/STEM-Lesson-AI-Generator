import os
import json
from typing import List, Dict, Any
from services.workspace.history.history_entry import HistoryEntry

class HistoryStore:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.history_file = os.path.join(storage_path, "history.json")

    def load_history(self) -> List[HistoryEntry]:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [HistoryEntry(**e) for e in data.get("entries", [])]
            except Exception:
                return []
        return []

    def save_history(self, entries: List[HistoryEntry]) -> None:
        data = {"entries": [e.model_dump() for e in entries]}
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
