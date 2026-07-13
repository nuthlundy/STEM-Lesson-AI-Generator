import time
import uuid
import hashlib
import os
from typing import List, Dict, Any, Optional
from services.workspace.snapshots.snapshot import Snapshot
from services.workspace.snapshots.snapshot_store import SnapshotStore
from services.workspace.snapshots.snapshot_validator import SnapshotValidator

class SnapshotManager:
    def __init__(self, storage_path: str = ".") -> None:
        self.store = SnapshotStore(storage_path=storage_path)
        self.snapshots: List[Snapshot] = self.store.load_snapshots()

    def _calculate_checksum(self, root_path: str) -> str:
        hasher = hashlib.md5()
        hasher.update(root_path.encode("utf-8"))
        return hasher.hexdigest()

    def create_snapshot(self, project_id: str, root_path: str, description: str) -> Snapshot:
        checksum = self._calculate_checksum(root_path)
        snap = Snapshot(
            snapshot_id=str(uuid.uuid4()),
            project_id=project_id,
            creation_timestamp=time.time(),
            description=description,
            workspace_checksum=checksum
        )
        self.snapshots.append(snap)
        self.store.save_snapshots(self.snapshots)
        return snap

    def restore_snapshot(self, snapshot_id: str, root_path: str) -> bool:
        for snap in self.snapshots:
            if snap.snapshot_id == snapshot_id:
                checksum = self._calculate_checksum(root_path)
                if SnapshotValidator.validate(snap, checksum):
                    return True
        return False

    def delete_snapshot(self, snapshot_id: str) -> bool:
        for i, snap in enumerate(self.snapshots):
            if snap.snapshot_id == snapshot_id:
                self.snapshots.pop(i)
                self.store.save_snapshots(self.snapshots)
                return True
        return False

    def list_snapshots(self) -> List[Snapshot]:
        return list(self.snapshots)
