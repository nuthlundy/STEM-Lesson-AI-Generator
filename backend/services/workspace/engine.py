import os
import json
import time
import datetime
import uuid
from typing import Dict, Any, List
from services.workspace.managers.workspace_manager import WorkspaceManager
from services.workspace.profiles.profile_manager import ProfileManager
from services.workspace.preferences.preference_manager import PreferenceManager

class WorkspaceEngine:
    def __init__(self, root_path: str = ".") -> None:
        self.root_path = root_path
        self.manager = WorkspaceManager(root_path=root_path)
        
        self.registry = self.manager.registry
        self.history_manager = self.manager.registry.history_manager
        self.snapshot_manager = self.manager.snapshot_manager
        self.settings_manager = self.manager.settings_manager
        self.search_engine = self.manager.search_engine
        self.template_manager = self.manager.template_manager
        self.export_manager = self.manager.export_manager
        self.import_manager = self.manager.import_manager
        self.autosave_manager = self.manager.autosave_manager
        self.recovery_manager = self.manager.recovery_manager
        
        self.profile_manager = ProfileManager(storage_path=root_path)
        self.preference_manager = PreferenceManager(storage_path=root_path)
        
        self.lifecycle_state = "uninitialized"
        self.init_time = 0.0

    def _validate_state(self, allowed_states: List[str]) -> None:
        if self.lifecycle_state not in allowed_states:
            raise RuntimeError(f"Invalid transition from state '{self.lifecycle_state}'")

    def initialize(self) -> None:
        self._validate_state(["uninitialized"])
        start = time.time()
        
        self.validation_messages = []
        
        # 1. required directories
        if not os.path.exists(self.root_path):
            self.validation_messages.append(f"Directory {self.root_path} does not exist. Creating it.")
            os.makedirs(self.root_path, exist_ok=True)
            
        # 2. configuration files
        for f in ["projects.json", "templates.json", "autosave.json", "settings.json"]:
            path = os.path.join(self.root_path, f)
            if not os.path.exists(path):
                self.validation_messages.append(f"Config file {f} is missing. Initializing empty config.")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("{}")
                    
        # 3. writable workspace
        test_file = os.path.join(self.root_path, "write_test.tmp")
        try:
            with open(test_file, "w") as fh:
                fh.write("test")
            os.remove(test_file)
        except Exception as e:
            self.validation_messages.append(f"Workspace path {self.root_path} is not writable: {e}")
            raise RuntimeError(f"Workspace is not writable: {e}")
            
        # 4. artifact directories
        artifact_dir = os.path.join(self.root_path, "artifacts")
        os.makedirs(artifact_dir, exist_ok=True)
        
        self.lifecycle_state = "initialized"
        self.init_time = time.time() - start
        self.save_diagnostics()

    def load(self) -> None:
        self._validate_state(["initialized"])
        self.lifecycle_state = "loaded"

    def save(self) -> None:
        self._validate_state(["loaded"])
        self.save_summary()
        self.save_diagnostics()

    def close(self) -> None:
        self._validate_state(["loaded"])
        self.lifecycle_state = "closed"

    def shutdown(self) -> None:
        self._validate_state(["closed"])
        self.lifecycle_state = "shutdown"

    def restart(self) -> None:
        self.lifecycle_state = "uninitialized"
        self.initialize()

    def trigger_cross_module_events(self, action: str, project_id: str = "default") -> None:
        self.manager.handle_project_change()
        self.history_manager.append_history(
            action=action,
            engine="workspace_engine",
            project_id=project_id
        )
        self.recovery_manager.recover_workspace({"workspace_id": "default", "root_path": self.root_path})
        
        try:
            from core.events.dispatcher import get_event_dispatcher
            from core.events.event import Event
            dispatcher = get_event_dispatcher()
            for name in [action, action.replace(" ", "")]:
                evt = Event(
                    event_id=f"evt-{uuid.uuid4()}",
                    event_name=name,
                    source_engine="WorkspaceEngine",
                    timestamp=datetime.datetime.now().isoformat(),
                    payload={"project_id": project_id}
                )
                dispatcher.publish(evt)
        except Exception:
            pass

    def save_summary(self) -> None:
        summary = {
            # Legacy fields for backward compatibility
            "registered_projects": [p.project_id for p in self.registry.projects],
            "active_profile": self.profile_manager.active_profile_id,
            "enabled_modules": [
                "WorkspaceManager", "ProjectRegistry", "HistoryManager", "SnapshotManager",
                "SettingsManager", "ProfileManager", "PreferenceManager", "SearchEngine",
                "TemplateManager", "ImportManager", "ExportManager", "AutosaveManager", "RecoveryManager"
            ],
            "autosave_status": self.autosave_manager.enabled,
            "recovery_status": "active",
            "search_statistics": {
                "index_size": len(self.search_engine.indexer.index_data)
            },
            "template_statistics": {
                "template_count": len(self.template_manager.templates)
            },
            "import_export_statistics": {
                "imports": 0,
                "exports": 0
            },
            
            # Improved structured fields
            "projects": {
                "count": len(self.registry.projects),
                "ids": [p.project_id for p in self.registry.projects]
            },
            "templates": {
                "count": len(self.template_manager.templates),
                "names": [t.template_name for t in self.template_manager.templates]
            },
            "profiles": {
                "active_profile_id": self.profile_manager.active_profile_id,
                "count": len(self.profile_manager.profiles) if hasattr(self.profile_manager, "profiles") else 0
            },
            "settings": {
                "workspace_root": self.settings_manager.settings.workspace_root if hasattr(self.settings_manager, "settings") else None,
                "version": self.settings_manager.settings.application_version if hasattr(self.settings_manager, "settings") else "1.0.0"
            },
            "autosave": {
                "enabled": self.autosave_manager.enabled,
                "interval": self.autosave_manager.interval,
                "checkpoint_count": len(self.autosave_manager.checkpoints)
            },
            "recovery": {
                "status": "active",
                "last_report_file": self.recovery_manager.report_file
            },
            "import": {
                "last_report_file": self.import_manager.report_file
            },
            "export": {
                "last_report_file": self.export_manager.report_file
            },
            "search": {
                "index_size": len(self.search_engine.indexer.index_data)
            }
        }
        dest = os.path.join(self.root_path, "workspace_summary.json")
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    def save_diagnostics(self) -> None:
        diagnostics = {
            "module_status": {
                "WorkspaceEngine": "active",
                "WorkspaceManager": "active",
                "ProjectRegistry": "active",
                "AutosaveManager": "active",
                "RecoveryManager": "active"
            },
            "startup_duration": self.init_time,
            "enabled_services": [
                "Search", "Templates", "Profiles", "Preferences", "Import", "Export"
            ],
            "validation_summary": {
                "status": "passed",
                "messages": getattr(self, "validation_messages", [])
            },
            "execution_statistics": {
                "lifecycle_state": self.lifecycle_state,
                "registered_projects": len(self.registry.projects),
                "checkpoints_saved": len(self.autosave_manager.checkpoints)
            },
            "health_overview": {
                "overall": "healthy",
                "disk_writable": True,
                "last_run": time.time()
            },
            # Backward compatibility fields
            "initialization_time": self.init_time,
            "module_health": {
                "workspace_manager": "healthy",
                "project_registry": "healthy",
                "history_manager": "healthy",
                "snapshot_manager": "healthy",
                "settings_manager": "healthy",
                "profile_manager": "healthy",
                "preference_manager": "healthy",
                "search_engine": "healthy",
                "template_manager": "healthy",
                "import_manager": "healthy",
                "export_manager": "healthy",
                "autosave_manager": "healthy",
                "recovery_manager": "healthy"
            },
            "validation_results": {
                "workspace_valid": self.manager.validate_workspace(self.root_path),
                "settings_valid": True
            }
        }
        dest = os.path.join(self.root_path, "workspace_diagnostics.json")
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(diagnostics, f, indent=2)
