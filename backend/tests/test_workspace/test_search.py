import unittest
import tempfile
import os
import time
from services.workspace.search.search_engine import SearchEngine
from services.workspace.managers.workspace_manager import WorkspaceManager
from services.workspace.registry.project_metadata import ProjectMetadata

class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.engine = SearchEngine(storage_path=self.storage_path)
        
        self.engine.indexer.index_item("p1", "Math Class", "Basic Algebra", "project", {"timestamp": 100.0, "priority": 5})
        self.engine.indexer.index_item("p2", "Science Lab", "Chemistry Experiments", "project", {"timestamp": 200.0, "priority": 10})

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_search_by_keyword(self):
        results = self.engine.search("Math")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "p1")

    def test_search_by_exact_match(self):
        results = self.engine.search("Math Class", exact=True)
        self.assertEqual(len(results), 1)

    def test_search_by_prefix(self):
        results = self.engine.search("Sci", prefix=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "p2")

    def test_ranking_relevance(self):
        results = self.engine.search("experiments")
        self.assertEqual(results[0]["id"], "p2")

    def test_ranking_recency(self):
        results = self.engine.search("Class", order_by="recency")
        self.assertTrue(len(results) > 0)

    def test_workspace_manager_automatic_refresh(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            ws_path = os.path.join(tmp_dir, "ws1")
            os.makedirs(ws_path, exist_ok=True)
            
            p = ProjectMetadata(
                project_id="proj-auto",
                project_name="Auto Project Name",
                creation_date=time.time(),
                last_modified=time.time(),
                workspace_path=ws_path
            )
            mgr.registry.register_project(p)
            
            res = mgr.search_engine.search("Auto")
            self.assertEqual(len(res), 1)
            self.assertEqual(res[0]["id"], "proj-auto")

if __name__ == "__main__":
    unittest.main()
