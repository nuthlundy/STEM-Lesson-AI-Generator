from services.workspace.managers.workspace_manager import WorkspaceManager

class WorkspaceFactory:
    @staticmethod
    def create_workspace_manager() -> WorkspaceManager:
        return WorkspaceManager()
