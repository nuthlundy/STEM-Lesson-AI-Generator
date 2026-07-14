import unittest
import tempfile
import os
import json
from services.workspace.engine import WorkspaceEngine
from core.health.report import PlatformHealthReporter
from core.documentation.generator import PlatformDocGenerator

class TestWorkspaceIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.storage_path = self.tmp_dir.name
        self.engine = WorkspaceEngine(root_path=self.storage_path)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_lifecycle_success_path(self):
        self.assertEqual(self.engine.lifecycle_state, "uninitialized")
        self.engine.initialize()
        self.assertEqual(self.engine.lifecycle_state, "initialized")
        self.engine.load()
        self.assertEqual(self.engine.lifecycle_state, "loaded")
        self.engine.save()
        self.assertEqual(self.engine.lifecycle_state, "loaded")
        self.engine.close()
        self.assertEqual(self.engine.lifecycle_state, "closed")
        self.engine.shutdown()
        self.assertEqual(self.engine.lifecycle_state, "shutdown")

    def test_lifecycle_restart(self):
        self.engine.initialize()
        self.engine.load()
        self.engine.restart()
        self.assertEqual(self.engine.lifecycle_state, "initialized")

    def test_lifecycle_invalid_transition_load(self):
        with self.assertRaises(RuntimeError):
            self.engine.load()

    def test_lifecycle_invalid_transition_save(self):
        with self.assertRaises(RuntimeError):
            self.engine.save()

    def test_lifecycle_invalid_transition_close(self):
        with self.assertRaises(RuntimeError):
            self.engine.close()

    def test_lifecycle_invalid_transition_shutdown(self):
        with self.assertRaises(RuntimeError):
            self.engine.shutdown()

    def test_module_integration_attributes(self):
        self.assertIsNotNone(self.engine.manager)
        self.assertIsNotNone(self.engine.registry)
        self.assertIsNotNone(self.engine.history_manager)
        self.assertIsNotNone(self.engine.snapshot_manager)
        self.assertIsNotNone(self.engine.settings_manager)
        self.assertIsNotNone(self.engine.search_engine)
        self.assertIsNotNone(self.engine.template_manager)
        self.assertIsNotNone(self.engine.export_manager)
        self.assertIsNotNone(self.engine.import_manager)
        self.assertIsNotNone(self.engine.autosave_manager)
        self.assertIsNotNone(self.engine.recovery_manager)

    def test_cross_module_events_trigger(self):
        self.engine.initialize()
        self.engine.load()
        self.engine.trigger_cross_module_events("test_action")
        self.assertTrue(len(self.engine.history_manager.entries) > 0)

    def test_diagnostics_generation(self):
        self.engine.initialize()
        diag_path = os.path.join(self.storage_path, "workspace_diagnostics.json")
        self.assertTrue(os.path.exists(diag_path))

    def test_cross_module_events_dispatch_bus(self):
        from core.events.dispatcher import get_event_dispatcher
        dispatcher = get_event_dispatcher()
        events = []
        dispatcher.subscribe("ProjectCreated", events.append)
        
        self.engine.initialize()
        self.engine.load()
        from services.workspace.registry.project_metadata import ProjectMetadata
        import time
        p = ProjectMetadata(
            project_id="event-proj",
            project_name="Math Event",
            creation_date=time.time(),
            last_modified=time.time(),
            workspace_path=self.storage_path
        )
        self.engine.registry.register_project(p)
        self.assertTrue(len(events) > 0)
        self.assertEqual(events[0].payload["project_id"], "event-proj")

    def test_diagnostics_content(self):
        self.engine.initialize()
        diag_path = os.path.join(self.storage_path, "workspace_diagnostics.json")
        self.engine.save_diagnostics()
        with open(diag_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("startup_duration", data)
        self.assertEqual(data["module_status"]["WorkspaceEngine"], "active")

    def test_summary_content_improved_fields(self):
        self.engine.initialize()
        self.engine.load()
        self.engine.save()
        summary_path = os.path.join(self.storage_path, "workspace_summary.json")
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("projects", data)
        self.assertIn("templates", data)
        self.assertIn("settings", data)
        self.assertIn("autosave", data)
        self.assertIn("recovery", data)

    def test_engine_initialization_with_custom_path(self):
        eng = WorkspaceEngine(root_path=self.storage_path)
        self.assertEqual(eng.root_path, self.storage_path)

    # Milestone 6B (Production Hardening) New Tests
    def test_diagnostics_expanded_fields(self):
        self.engine.initialize()
        diag_path = os.path.join(self.storage_path, "workspace_diagnostics.json")
        with open(diag_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("module_status", data)
        self.assertIn("startup_duration", data)
        self.assertIn("enabled_services", data)
        self.assertIn("validation_summary", data)
        self.assertIn("execution_statistics", data)
        self.assertIn("health_overview", data)

    def test_startup_required_directories_exist(self):
        non_existent_dir = os.path.join(self.storage_path, "sub_new_folder")
        eng = WorkspaceEngine(root_path=non_existent_dir)
        eng.initialize()
        self.assertTrue(os.path.exists(non_existent_dir))

    def test_startup_required_config_files_exist(self):
        self.engine.initialize()
        for f in ["projects.json", "templates.json", "autosave.json", "settings.json"]:
            self.assertTrue(os.path.exists(os.path.join(self.storage_path, f)))

    def test_startup_non_writable_workspace(self):
        # We simulate a non-writable path by pointing to an invalid directory or simulating it
        # Under windows, pointing to a read-only area or invalid system path raises RuntimeError
        invalid_path = "Z:\\non_existent_drive_faked"
        eng = WorkspaceEngine(root_path=invalid_path)
        with self.assertRaises(Exception):
            eng.initialize()

    def test_startup_artifact_directory_created(self):
        self.engine.initialize()
        self.assertTrue(os.path.exists(os.path.join(self.storage_path, "artifacts")))

    def test_health_reporter_includes_workspace(self):
        report = PlatformHealthReporter.generate_report(workspace_root=self.storage_path)
        self.assertIn("Workspace", report["health"]["subsystems"])
        self.assertIn("Rendering", report["health"]["subsystems"])
        self.assertIn("Presentation", report["health"]["subsystems"])

    def test_platform_doc_generator_includes_module_inventory(self):
        summary = PlatformDocGenerator.generate_summary(workspace_root=self.storage_path)
        self.assertIn("module_inventory", summary)
        self.assertIn("workspace", summary["module_inventory"])

    def test_platform_doc_generator_includes_service_inventory(self):
        summary = PlatformDocGenerator.generate_summary(workspace_root=self.storage_path)
        self.assertIn("service_inventory", summary)
        self.assertIn("WorkspaceEngine", summary["service_inventory"])

    def test_platform_doc_generator_includes_production_readiness(self):
        summary = PlatformDocGenerator.generate_summary(workspace_root=self.storage_path)
        self.assertIn("production_readiness_summary", summary)
        self.assertEqual(summary["production_readiness_summary"]["status"], "ready")

    def test_lifecycle_reinitialization_failure(self):
        self.engine.initialize()
        with self.assertRaises(RuntimeError):
            self.engine.initialize()

if __name__ == "__main__":
    unittest.main()
