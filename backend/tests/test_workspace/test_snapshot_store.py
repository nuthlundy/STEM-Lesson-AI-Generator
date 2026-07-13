import unittest
import tempfile
import os
from services.workspace.snapshots.snapshot_store import SnapshotStore
from services.workspace.snapshots.snapshot import Snapshot
from services.workspace.snapshots.snapshot_validator import SnapshotValidator

class TestSnapshotStore(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.store = SnapshotStore(storage_path=self.storage_path)
        self.snap = Snapshot(
            snapshot_id="s1",
            project_id="p1",
            creation_timestamp=12345.6,
            description="Backup",
            workspace_checksum="hash1"
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_save_and_load_snapshots(self):
        self.store.save_snapshots([self.snap])
        loaded = self.store.load_snapshots()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].snapshot_id, "s1")

    def test_load_empty_store(self):
        self.assertEqual(self.store.load_snapshots(), [])

    def test_load_corrupted_json(self):
        with open(self.store.snapshots_file, "w") as f:
            f.write("{invalid json")
        self.assertEqual(self.store.load_snapshots(), [])

    def test_validator_success(self):
        self.assertTrue(SnapshotValidator.validate(self.snap, "hash1"))

    def test_validator_checksum_mismatch(self):
        self.assertFalse(SnapshotValidator.validate(self.snap, "hash2"))

    def test_validator_empty_ids(self):
        invalid_snap = Snapshot(
            snapshot_id="",
            project_id="",
            creation_timestamp=0.0,
            description="",
            workspace_checksum=""
        )
        self.assertFalse(SnapshotValidator.validate(invalid_snap, ""))

if __name__ == "__main__":
    unittest.main()
