from typing import List
from services.workspace.history.history_entry import HistoryEntry

class HistoryQuery:
    @staticmethod
    def latest(entries: List[HistoryEntry], limit: int = 10) -> List[HistoryEntry]:
        return sorted(entries, key=lambda e: e.timestamp, reverse=True)[:limit]

    @staticmethod
    def by_project(entries: List[HistoryEntry], project_id: str) -> List[HistoryEntry]:
        return [e for e in entries if e.project_id == project_id]

    @staticmethod
    def by_engine(entries: List[HistoryEntry], engine: str) -> List[HistoryEntry]:
        return [e for e in entries if e.engine == engine]

    @staticmethod
    def by_date(entries: List[HistoryEntry], start_time: float, end_time: float) -> List[HistoryEntry]:
        return [e for e in entries if start_time <= e.timestamp <= end_time]
