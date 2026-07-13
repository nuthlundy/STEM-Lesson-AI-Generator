import os
from services.workspace.snapshots.snapshot import Snapshot

class SnapshotValidator:
    @staticmethod
    def validate(snapshot: Snapshot, expected_checksum: str) -> bool:
        if not snapshot.snapshot_id or not snapshot.project_id:
            return False
        if snapshot.workspace_checksum != expected_checksum:
            return False
        return True
