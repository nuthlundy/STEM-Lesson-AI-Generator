import os
import json
from typing import List
from services.workspace.snapshots.snapshot import Snapshot

class SnapshotStore:
    def __init__(self, storage_path: str = ".") -> None:
        self.storage_path = storage_path
        self.snapshots_file = os.path.join(storage_path, "snapshots.json")

    def load_snapshots(self) -> List[Snapshot]:
        if os.path.exists(self.snapshots_file):
            try:
                with open(self.snapshots_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return [Snapshot(**s) for s in data.get("snapshots", [])]
            except Exception:
                return []
        return []

    def save_snapshots(self, snapshots: List[Snapshot]) -> None:
        data = {"snapshots": [s.model_dump() for s in snapshots]}
        with open(self.snapshots_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
