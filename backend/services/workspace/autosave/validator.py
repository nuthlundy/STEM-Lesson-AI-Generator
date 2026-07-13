import os
from services.workspace.autosave.checkpoint import AutosaveCheckpoint

class AutosaveValidator:
    @staticmethod
    def validate_checkpoint(checkpoint: AutosaveCheckpoint) -> bool:
        if not checkpoint.checkpoint_id or not checkpoint.project_id:
            return False
        if checkpoint.timestamp <= 0.0:
            return False
        return True
