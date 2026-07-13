import unittest
import tempfile
import os
from services.workspace.search.indexer import SearchIndexer

class TestSearchIndexer(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.indexer = SearchIndexer(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_index_item_saves_file(self):
        self.indexer.index_item("i1", "Title", "Desc", "lesson")
        self.assertTrue(os.path.exists(self.indexer.index_file))
        self.assertEqual(len(self.indexer.index_data), 1)

    def test_index_item_overwrites_existing(self):
        self.indexer.index_item("i1", "Old Title", "Old Desc", "lesson")
        self.indexer.index_item("i1", "New Title", "New Desc", "lesson")
        self.assertEqual(len(self.indexer.index_data), 1)
        self.assertEqual(self.indexer.index_data[0]["name"], "New Title")

    def test_clear_index(self):
        self.indexer.index_item("i1", "Title", "Desc", "lesson")
        self.indexer.clear()
        self.assertEqual(len(self.indexer.index_data), 0)

    def test_load_empty_indexer(self):
        new_indexer = SearchIndexer(storage_path="nonexistent_folder_faking")
        self.assertEqual(len(new_indexer.index_data), 0)

    def test_load_corrupted_json(self):
        with open(self.indexer.index_file, "w") as f:
            f.write("{corrupt")
        self.indexer.load_index()
        self.assertEqual(len(self.indexer.index_data), 0)

    def test_index_with_extra_metadata(self):
        self.indexer.index_item("i1", "Title", "Desc", "lesson", {"timestamp": 123.4, "priority": 10})
        self.assertEqual(self.indexer.index_data[0]["timestamp"], 123.4)
        self.assertEqual(self.indexer.index_data[0]["priority"], 10)

if __name__ == "__main__":
    unittest.main()
