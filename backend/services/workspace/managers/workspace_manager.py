import os
import json
import time
import uuid
import importlib
from typing import Dict, Any, List
from services.workspace.schemas import WorkspaceMetadata
from services.workspace.managers.directory_manager import DirectoryManager
from services.workspace.registry.project_registry import ProjectRegistry
from services.workspace.snapshots.snapshot_manager import SnapshotManager
from services.workspace.settings.settings_manager import SettingsManager
from services.workspace.search.search_engine import SearchEngine
from services.workspace.templates.template_manager import TemplateManager

class WorkspaceManager:
    def __init__(self, root_path: str = ".") -> None:
        self.root_path = root_path
        self.active_workspaces: Dict[str, WorkspaceMetadata] = {}
        self.search_engine = SearchEngine(storage_path=root_path)
        self.registry = ProjectRegistry(storage_path=root_path, on_change_callback=self.refresh_search_index)
        self.snapshot_manager = SnapshotManager(storage_path=root_path, on_change_callback=self.refresh_search_index)
        self.settings_manager = SettingsManager(storage_path=root_path)
        self.template_manager = TemplateManager(storage_path=root_path, on_change_callback=self.refresh_search_index)
        
        import_mod = importlib.import_module("services.workspace.import.import_manager")
        self.import_manager = import_mod.ImportManager(storage_path=root_path)

    def create_workspace(self, root_path: str, directories: List[str]) -> WorkspaceMetadata:
        workspace_id = str(uuid.uuid4())
        DirectoryManager.create_directories(root_path, directories)
        
        meta = WorkspaceMetadata(
            workspace_id=workspace_id,
            root_path=root_path,
            created_at=time.time(),
            status="active",
            directories=directories
        )
        
        config_path = os.path.join(root_path, "workspace.json")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(meta.model_dump(), f, indent=2)
            
        self.active_workspaces[workspace_id] = meta
        self.refresh_search_index()
        return meta

    def open_workspace(self, root_path: str) -> WorkspaceMetadata:
        config_path = os.path.join(root_path, "workspace.json")
        if not os.path.exists(config_path):
            raise ValueError("Workspace config workspace.json not found")
            
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        meta = WorkspaceMetadata(**data)
        self.active_workspaces[meta.workspace_id] = meta
        return meta

    def close_workspace(self, workspace_id: str) -> None:
        if workspace_id in self.active_workspaces:
            meta = self.active_workspaces[workspace_id]
            meta.status = "closed"
            config_path = os.path.join(meta.root_path, "workspace.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(meta.model_dump(), f, indent=2)
            del self.active_workspaces[workspace_id]

    def validate_workspace(self, root_path: str) -> bool:
        config_path = os.path.join(root_path, "workspace.json")
        if not os.path.exists(config_path):
            return False
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            meta = WorkspaceMetadata(**data)
            return DirectoryManager.verify_structure(root_path, meta.directories)
        except Exception:
            return False

    def create_snapshot(self, project_id: str, description: str) -> Any:
        snap = self.snapshot_manager.create_snapshot(project_id, self.root_path, description)
        self.registry.history_manager.log_snapshot_creation(project_id, snap.snapshot_id)
        return snap

    def restore_snapshot(self, snapshot_id: str) -> bool:
        project_id = "unknown"
        for snap in self.snapshot_manager.snapshots:
            if snap.snapshot_id == snapshot_id:
                project_id = snap.project_id
                break
        res = self.snapshot_manager.restore_snapshot(snapshot_id, self.root_path)
        if res:
            self.registry.history_manager.log_snapshot_restore(project_id, snapshot_id)
        return res

    def create_template(self, name: str, category: str, description: str, curriculum: str = "NGSS", grades: List[str] = None) -> Any:
        return self.template_manager.create_template(name, category, description, curriculum, grades)

    def apply_template(self, template_id: str, project_id: str) -> bool:
        return self.template_manager.apply_template(template_id, project_id)

    def import_project(self, file_path: str) -> Dict[str, Any]:
        res = self.import_manager.import_project(file_path)
        self.refresh_search_index()
        return res

    def import_workspace(self, file_path: str) -> Dict[str, Any]:
        res = self.import_manager.import_workspace(file_path)
        self.refresh_search_index()
        return res

    def refresh_search_index(self) -> None:
        self.search_engine.indexer.clear()
        for p in self.registry.projects:
            self.search_engine.indexer.index_item(
                item_id=p.project_id,
                name=p.project_name,
                description=f"Workspace path: {p.workspace_path}",
                category="project",
                extra={"timestamp": p.creation_date}
            )
        for s in self.snapshot_manager.snapshots:
            self.search_engine.indexer.index_item(
                item_id=s.snapshot_id,
                name=s.description,
                description=f"Snapshot for project: {s.project_id}",
                category="snapshot",
                extra={"timestamp": s.creation_timestamp}
            )
        for t in self.template_manager.templates:
            self.search_engine.indexer.index_item(
                item_id=t.template_id,
                name=t.template_name,
                description=t.description,
                category="template",
                extra={"timestamp": t.created_timestamp}
            )
        self.search_engine.indexer.save_index()
