import unittest
import time
from services.workspace.registry.project_metadata import ProjectMetadata

class TestProjectMetadata(unittest.TestCase):
    def setUp(self):
        self.now = time.time()
        self.meta = ProjectMetadata(
            project_id="p1",
            project_name="Math Lesson",
            creation_date=self.now,
            last_modified=self.now,
            workspace_path="/path/to/workspace"
        )

    def test_metadata_fields(self):
        self.assertEqual(self.meta.project_id, "p1")
        self.assertEqual(self.meta.project_name, "Math Lesson")
        self.assertEqual(self.meta.creation_date, self.now)
        self.assertEqual(self.meta.last_modified, self.now)
        self.assertEqual(self.meta.workspace_path, "/path/to/workspace")

    def test_metadata_defaults(self):
        self.assertEqual(self.meta.version, "1.0.0")
        self.assertEqual(self.meta.engine_compatibility, ">=1.0.0")

    def test_metadata_dict_serialization(self):
        d = self.meta.model_dump()
        self.assertEqual(d["project_id"], "p1")
        self.assertEqual(d["version"], "1.0.0")

    def test_metadata_validation(self):
        meta_dict = self.meta.model_dump()
        restored = ProjectMetadata(**meta_dict)
        self.assertEqual(restored.project_name, "Math Lesson")

    def test_metadata_modification(self):
        self.meta.project_name = "New Name"
        self.assertEqual(self.meta.project_name, "New Name")

    def test_metadata_version_update(self):
        self.meta.version = "2.0.0"
        self.assertEqual(self.meta.version, "2.0.0")

    def test_metadata_compatibility_update(self):
        self.meta.engine_compatibility = ">=2.0.0"
        self.assertEqual(self.meta.engine_compatibility, ">=2.0.0")

    def test_metadata_last_modified_update(self):
        new_time = time.time() + 10
        self.meta.last_modified = new_time
        self.assertEqual(self.meta.last_modified, new_time)

if __name__ == "__main__":
    unittest.main()
