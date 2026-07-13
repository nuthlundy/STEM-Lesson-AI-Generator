import os
import json
from typing import List, Dict, Any

class SearchIndexer:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.index_file = os.path.join(storage_path, "search_index.json")
        self.index_data: List[Dict[str, Any]] = []
        self.load_index()

    def load_index(self) -> None:
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    self.index_data = json.load(f)
            except Exception:
                self.index_data = []

    def save_index(self) -> None:
        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(self.index_data, f, indent=2)

    def index_item(self, item_id: str, name: str, description: str, category: str, extra: Dict[str, Any] = None) -> None:
        self.index_data = [item for item in self.index_data if item.get("id") != item_id]
        
        doc = {
            "id": item_id,
            "name": name,
            "description": description,
            "category": category,
            "timestamp": extra.get("timestamp", 0.0) if extra else 0.0,
            "priority": extra.get("priority", 0) if extra else 0,
            "extra": extra or {}
        }
        self.index_data.append(doc)
        self.save_index()

    def clear(self) -> None:
        self.index_data.clear()
        self.save_index()
