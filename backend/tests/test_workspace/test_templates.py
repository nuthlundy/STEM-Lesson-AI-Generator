import unittest
import tempfile
import os
from services.workspace.templates.template_manager import TemplateManager
from services.workspace.templates.template import LessonTemplate
from services.workspace.managers.workspace_manager import WorkspaceManager

class TestTemplateManager(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.manager = TemplateManager(storage_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_create_template_success(self):
        t = self.manager.create_template("Math Template", "Stem", "Basic Math structure")
        self.assertIsNotNone(t)
        self.assertEqual(t.template_name, "Math Template")
        self.assertEqual(len(self.manager.templates), 1)

    def test_create_template_duplicate_name_failure(self):
        self.manager.create_template("Math Template", "Stem", "Basic Math structure")
        t = self.manager.create_template("Math Template", "Stem", "Another one")
        self.assertIsNone(t)

    def test_update_template_success(self):
        t = self.manager.create_template("Math Template", "Stem", "Basic Math structure")
        self.assertTrue(self.manager.update_template(t.template_id, {"description": "New Desc"}))
        self.assertEqual(self.manager.templates[0].description, "New Desc")

    def test_update_template_validation_failure(self):
        t = self.manager.create_template("Math Template", "Stem", "Basic Math structure")
        self.assertFalse(self.manager.update_template(t.template_id, {"supported_curriculum": "unsupported"}))

    def test_delete_template(self):
        t = self.manager.create_template("Math Template", "Stem", "Basic Math structure")
        self.assertTrue(self.manager.delete_template(t.template_id))
        self.assertEqual(len(self.manager.templates), 0)

    def test_apply_template(self):
        t = self.manager.create_template("Math Template", "Stem", "Basic Math structure")
        self.assertTrue(self.manager.apply_template(t.template_id, "proj-1"))

    def test_list_templates(self):
        self.manager.create_template("Math Template", "Stem", "Basic Math structure")
        self.assertEqual(len(self.manager.list_templates()), 1)

    def test_workspace_manager_template_search_indexing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mgr = WorkspaceManager(root_path=tmp_dir)
            t = mgr.create_template("Stem Physics", "Science", "Physics design")
            
            results = mgr.search_engine.search_templates("Physics")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["id"], t.template_id)

if __name__ == "__main__":
    unittest.main()
