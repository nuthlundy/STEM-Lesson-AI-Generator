import time
from typing import List, Dict, Any
from services.workspace.history.history_entry import HistoryEntry
from services.workspace.history.history_store import HistoryStore
from services.workspace.history.history_query import HistoryQuery

class HistoryManager:
    def __init__(self, storage_path: str = ".") -> None:
        self.store = HistoryStore(storage_path=storage_path)
        self.entries: List[HistoryEntry] = self.store.load_history()

    def append_history(self, action: str, engine: str, project_id: str, artifact: str = None, user_metadata: Dict[str, Any] = None) -> HistoryEntry:
        entry = HistoryEntry(
            timestamp=time.time(),
            action=action,
            engine=engine,
            artifact=artifact,
            project_id=project_id,
            user_metadata=user_metadata or {}
        )
        self.entries.append(entry)
        self.store.save_history(self.entries)
        return entry

    def retrieve_history(self) -> List[HistoryEntry]:
        return list(self.entries)

    def clear_history(self) -> None:
        self.entries.clear()
        self.store.save_history(self.entries)

    def filter_history(self, project_id: str = None, engine: str = None) -> List[HistoryEntry]:
        results = self.entries
        if project_id:
            results = HistoryQuery.by_project(results, project_id)
        if engine:
            results = HistoryQuery.by_engine(results, engine)
        return results

    def log_snapshot_creation(self, project_id: str, snapshot_id: str) -> None:
        self.append_history(
            action="snapshot_create",
            engine="workspace_manager",
            project_id=project_id,
            artifact=f"snapshot_{snapshot_id}"
        )

    def log_snapshot_restore(self, project_id: str, snapshot_id: str) -> None:
        self.append_history(
            action="snapshot_restore",
            engine="workspace_manager",
            project_id=project_id,
            artifact=f"snapshot_{snapshot_id}"
        )

    def log_snapshot_deletion(self, project_id: str, snapshot_id: str) -> None:
        self.append_history(
            action="snapshot_delete",
            engine="workspace_manager",
            project_id=project_id,
            artifact=f"snapshot_{snapshot_id}"
        )

