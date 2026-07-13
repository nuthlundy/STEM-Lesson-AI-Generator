from services.workspace.managers.workspace_manager import WorkspaceManager

class WorkspaceEngine:
    def __init__(self) -> None:
        self.manager = WorkspaceManager()
