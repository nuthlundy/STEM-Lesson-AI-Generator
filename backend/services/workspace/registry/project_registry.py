import os
import json
import time
import datetime
import uuid
from typing import Dict, List, Any, Optional
from services.workspace.registry.project_metadata import ProjectMetadata
from services.workspace.registry.project_validator import ProjectValidator
from services.workspace.registry.project_index import ProjectIndex
from services.workspace.history.history_manager import HistoryManager
from core.events.dispatcher import get_event_dispatcher
from core.events.event import Event

class ProjectRegistry:
    def __init__(self, storage_path: str = ".", on_change_callback = None) -> None:
        self.storage_path = storage_path
        self.projects_file = os.path.join(storage_path, "projects.json")
        self.projects: List[ProjectMetadata] = []
        self.index = ProjectIndex()
        self.history_manager = HistoryManager(storage_path=storage_path)
        self.on_change_callback = on_change_callback
        self.load_registry()

    def load_registry(self) -> None:
        if os.path.exists(self.projects_file):
            try:
                with open(self.projects_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.projects = [ProjectMetadata(**p) for p in data.get("projects", [])]
                for p in self.projects:
                    self.index.index_project(p)
            except Exception:
                self.projects = []

    def save_registry(self) -> None:
        data = {"projects": [p.model_dump() for p in self.projects]}
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def register_project(self, meta: ProjectMetadata) -> bool:
        if not ProjectValidator.validate(meta, self.projects):
            return False
        self.projects.append(meta)
        self.index.index_project(meta)
        self.save_registry()
        
        self.history_manager.append_history(
            action="create",
            engine="workspace_manager",
            project_id=meta.project_id,
            artifact="workspace.json"
        )
        
        try:
            dispatcher = get_event_dispatcher()
            for event_name in ["ProjectCreated", "Project Created"]:
                evt = Event(
                    event_id=f"evt-{uuid.uuid4()}",
                    event_name=event_name,
                    source_engine="WorkspaceEngine",
                    timestamp=datetime.datetime.now().isoformat(),
                    payload={"project_id": meta.project_id}
                )
                dispatcher.publish(evt)
        except Exception:
            pass

        if self.on_change_callback:
            self.on_change_callback()
        return True

    def unregister_project(self, project_id: str) -> bool:
        for i, p in enumerate(self.projects):
            if p.project_id == project_id:
                self.projects.pop(i)
                self.index.remove_project(project_id)
                self.save_registry()
                
                self.history_manager.append_history(
                    action="remove",
                    engine="workspace_manager",
                    project_id=project_id
                )
                if self.on_change_callback:
                    self.on_change_callback()
                return True
        return False

    def update_project(self, project_id: str, updates: Dict[str, Any]) -> bool:
        for p in self.projects:
            if p.project_id == project_id:
                for k, v in updates.items():
                    if hasattr(p, k):
                        setattr(p, k, v)
                p.last_modified = time.time()
                self.index.index_project(p)
                self.save_registry()
                
                self.history_manager.append_history(
                    action="update",
                    engine="workspace_manager",
                    project_id=project_id
                )
                
                try:
                    dispatcher = get_event_dispatcher()
                    for event_name in ["ProjectUpdated", "Project Updated"]:
                        evt = Event(
                            event_id=f"evt-{uuid.uuid4()}",
                            event_name=event_name,
                            source_engine="WorkspaceEngine",
                            timestamp=datetime.datetime.now().isoformat(),
                            payload={"project_id": project_id}
                        )
                        dispatcher.publish(evt)
                except Exception:
                    pass

                if self.on_change_callback:
                    self.on_change_callback()
                return True
        return False

    def lookup_project(self, project_id: str) -> Optional[ProjectMetadata]:
        return self.index.lookup(project_id)


    def get_export_metadata(self, project_id: str) -> Optional[Dict[str, Any]]:
        p = self.lookup_project(project_id)
        if p:
            return {
                "project_id": p.project_id,
                "project_name": p.project_name,
                "version": p.version,
                "engine_compatibility": p.engine_compatibility,
                "workspace_path": p.workspace_path
            }
        return None
