import unittest
import tempfile
import os
import time
from services.workspace.history.history_manager import HistoryManager
from services.workspace.history.history_entry import HistoryEntry
from services.workspace.history.history_store import HistoryStore

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = HistoryManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_append_history(self):
        entry = self.manager.append_history(action="test", engine="test_engine", project_id="p1")
        self.assertEqual(entry.action, "test")
        self.assertEqual(entry.engine, "test_engine")
        self.assertEqual(entry.project_id, "p1")
        self.assertEqual(len(self.manager.entries), 1)

    def test_retrieve_history(self):
        self.manager.append_history(action="test", engine="test_engine", project_id="p1")
        history = self.manager.retrieve_history()
        self.assertEqual(len(history), 1)

    def test_clear_history(self):
        self.manager.append_history(action="test", engine="test_engine", project_id="p1")
        self.manager.clear_history()
        self.assertEqual(len(self.manager.entries), 0)

    def test_filter_history_by_project(self):
        self.manager.append_history(action="test", engine="test_engine", project_id="p1")
        self.manager.append_history(action="test", engine="test_engine", project_id="p2")
        filtered = self.manager.filter_history(project_id="p1")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].project_id, "p1")

    def test_filter_history_by_engine(self):
        self.manager.append_history(action="test", engine="engine1", project_id="p1")
        self.manager.append_history(action="test", engine="engine2", project_id="p1")
        filtered = self.manager.filter_history(engine="engine1")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].engine, "engine1")

    def test_history_store_empty_load(self):
        store = HistoryStore(storage_path="nonexistent_folder_faking")
        self.assertEqual(store.load_history(), [])

    def test_history_entry_dump(self):
        entry = HistoryEntry(timestamp=time.time(), action="t", engine="e", project_id="p")
        self.assertEqual(entry.model_dump()["action"], "t")

    def test_history_manager_multiple_appends(self):
        self.manager.append_history(action="1", engine="e", project_id="p")
        self.manager.append_history(action="2", engine="e", project_id="p")
        self.assertEqual(len(self.manager.entries), 2)

if __name__ == "__main__":
    unittest.main()
