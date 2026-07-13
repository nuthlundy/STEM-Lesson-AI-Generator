import unittest
import time
from services.workspace.history.history_entry import HistoryEntry
from services.workspace.history.history_query import HistoryQuery

class TestHistoryQuery(unittest.TestCase):
    def setUp(self):
        self.entries = [
            HistoryEntry(timestamp=100.0, action="create", engine="eng1", project_id="p1"),
            HistoryEntry(timestamp=200.0, action="update", engine="eng2", project_id="p1"),
            HistoryEntry(timestamp=300.0, action="remove", engine="eng1", project_id="p2")
        ]

    def test_query_latest(self):
        latest = HistoryQuery.latest(self.entries, limit=2)
        self.assertEqual(len(latest), 2)
        self.assertEqual(latest[0].timestamp, 300.0)

    def test_query_by_project(self):
        p1_entries = HistoryQuery.by_project(self.entries, "p1")
        self.assertEqual(len(p1_entries), 2)
        self.assertEqual(p1_entries[0].project_id, "p1")

    def test_query_by_engine(self):
        eng1_entries = HistoryQuery.by_engine(self.entries, "eng1")
        self.assertEqual(len(eng1_entries), 2)
        self.assertEqual(eng1_entries[0].engine, "eng1")

    def test_query_by_date(self):
        date_entries = HistoryQuery.by_date(self.entries, 150.0, 250.0)
        self.assertEqual(len(date_entries), 1)
        self.assertEqual(date_entries[0].timestamp, 200.0)

    def test_query_latest_limit_exceeds(self):
        latest = HistoryQuery.latest(self.entries, limit=10)
        self.assertEqual(len(latest), 3)

    def test_query_by_project_nonexistent(self):
        self.assertEqual(HistoryQuery.by_project(self.entries, "p99"), [])

    def test_query_by_engine_nonexistent(self):
        self.assertEqual(HistoryQuery.by_engine(self.entries, "eng99"), [])

    def test_query_by_date_out_of_range(self):
        self.assertEqual(HistoryQuery.by_date(self.entries, 400.0, 500.0), [])

if __name__ == "__main__":
    unittest.main()
