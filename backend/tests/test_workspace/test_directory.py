import unittest
import tempfile
import os
from services.workspace.managers.directory_manager import DirectoryManager

class TestDirectoryManager(unittest.TestCase):
    def setUp(self):
        self.dirs = ["sub1", "sub2", "sub2/nested"]

    def test_create_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            DirectoryManager.create_directories(tmp_dir, self.dirs)
            self.assertTrue(os.path.isdir(os.path.join(tmp_dir, "sub1")))
            self.assertTrue(os.path.isdir(os.path.join(tmp_dir, "sub2/nested")))

    def test_verify_structure_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            DirectoryManager.create_directories(tmp_dir, self.dirs)
            self.assertTrue(DirectoryManager.verify_structure(tmp_dir, self.dirs))

    def test_verify_structure_failure(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            DirectoryManager.create_directories(tmp_dir, self.dirs)
            os.rmdir(os.path.join(tmp_dir, "sub2/nested"))
            self.assertFalse(DirectoryManager.verify_structure(tmp_dir, self.dirs))

    def test_cleanup_removes_directories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target_dir = os.path.join(tmp_dir, "to_delete")
            DirectoryManager.create_directories(target_dir, self.dirs)
            self.assertTrue(os.path.exists(target_dir))
            DirectoryManager.cleanup(target_dir)
            self.assertFalse(os.path.exists(target_dir))

    def test_create_directories_empty(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            DirectoryManager.create_directories(tmp_dir, [])
            self.assertTrue(DirectoryManager.verify_structure(tmp_dir, []))

    def test_verify_structure_empty(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.assertTrue(DirectoryManager.verify_structure(tmp_dir, []))

    def test_cleanup_nonexistent(self):
        DirectoryManager.cleanup("nonexistent_path_completely_fake")

    def test_create_directories_already_exists(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            DirectoryManager.create_directories(tmp_dir, self.dirs)
            DirectoryManager.create_directories(tmp_dir, self.dirs)
            self.assertTrue(DirectoryManager.verify_structure(tmp_dir, self.dirs))

if __name__ == "__main__":
    unittest.main()
