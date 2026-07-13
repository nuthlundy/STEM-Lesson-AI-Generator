import os
import json
import time
import uuid
import hashlib
from typing import List, Dict, Any, Optional
from services.workspace.autosave.checkpoint import AutosaveCheckpoint
from services.workspace.autosave.validator import AutosaveValidator
from services.workspace.autosave.scheduler import AutosaveScheduler

class AutosaveManager:
    def __init__(self, storage_path: str = ".", interval: float = 60.0, trigger_callback = None) -> None:
        self.storage_path = storage_path
        self.config_file = os.path.join(storage_path, "autosave.json")
        self.checkpoints: List[AutosaveCheckpoint] = []
        self.enabled = False
        self.interval = interval
        self.trigger_callback = trigger_callback
        self.scheduler = AutosaveScheduler(interval=interval, callback=self.trigger_autosave)
        self.load_config()

    def load_config(self) -> None:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.enabled = data.get("enabled_status", False)
                self.interval = data.get("interval", 60.0)
                self.scheduler.interval = self.interval
                self.checkpoints = [AutosaveCheckpoint(**c) for c in data.get("checkpoints", [])]
                if self.enabled:
                    self.scheduler.start()
            except Exception:
                pass

    def save_config(self) -> None:
        data = {
            "last_autosave": self.checkpoints[-1].timestamp if self.checkpoints else 0.0,
            "interval": self.interval,
            "enabled_status": self.enabled,
            "checkpoint_count": len(self.checkpoints),
            "checkpoints": [c.model_dump() for c in self.checkpoints]
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def enable_autosave(self) -> None:
        self.enabled = True
        self.scheduler.start()
        self.save_config()

    def disable_autosave(self) -> None:
        self.enabled = False
        self.scheduler.stop()
        self.save_config()

    def trigger_autosave(self, project_id: str = "default") -> Optional[AutosaveCheckpoint]:
        if self.trigger_callback:
            try:
                self.trigger_callback()
            except Exception:
                pass
        
        hasher = hashlib.md5()
        hasher.update(str(time.time()).encode("utf-8"))
        chk = AutosaveCheckpoint(
            checkpoint_id=str(uuid.uuid4()),
            timestamp=time.time(),
            project_id=project_id,
            changed_artifacts=["workspace.json"],
            checksum=hasher.hexdigest()
        )
        
        if AutosaveValidator.validate_checkpoint(chk):
            self.checkpoints.append(chk)
            self.save_config()
            return chk
        return None

    def restore_latest_autosave(self) -> bool:
        if not self.checkpoints:
            return False
        latest = self.checkpoints[-1]
        return AutosaveValidator.validate_checkpoint(latest)
