import os

class ArtifactResolver:
    """Resolves relative and absolute artifact file paths within the workspace."""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        
    def resolve_path(self, relative_path: str) -> str:
        """Returns the absolute path for a given workspace-relative path."""
        normalized_rel = relative_path.replace("\\", "/")
        if normalized_rel.startswith("/"):
            normalized_rel = normalized_rel[1:]
        return os.path.abspath(os.path.join(self.workspace_root, normalized_rel))
        
    def exists(self, relative_path: str) -> bool:
        """Checks if the artifact file physically exists on the disk."""
        return os.path.exists(self.resolve_path(relative_path))
