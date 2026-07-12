import unittest
import os
import json
import tempfile
from core.diagnostics import (
    get_diagnostics_manager,
    DiagnosticsManager,
    DiagnosticsValidator,
    PluginInspector,
    DiagnosticsReporter
)
from core.diagnostics.exceptions import DuplicateProviderError, BrokenProviderError
from core.plugins.registry import PluginRegistry
from core.plugins.plugin import BasePlugin
from typing import Dict, Any

class MockGoodPlugin(BasePlugin):
    def initialize(self) -> None: pass
    def execute(self, context: Dict[str, Any]) -> Any: pass
    def shutdown(self) -> None: pass
    def metadata(self) -> Dict[str, Any]:
        return {"id": "good", "name": "Good", "version": "1.0.0", "type": "Test"}

class MockBadPlugin(BasePlugin):
    def initialize(self) -> None: pass
    def execute(self, context: Dict[str, Any]) -> Any: pass
    def shutdown(self) -> None: pass
    def metadata(self) -> Dict[str, Any]:
        return {"id": "bad"} # missing keys

class TestDiagnostics(unittest.TestCase):
    def setUp(self):
        from core.diagnostics.diagnostics import DiagnosticsManager
        self.manager = DiagnosticsManager()

    def test_provider_registration(self):
        self.manager.register_provider("p1", lambda: {"status": "OK"})
        self.assertIn("p1", self.manager.list_providers())
        res = self.manager.run_all()
        self.assertEqual(res["p1"]["status"], "OK")

    def test_duplicate_provider_registration(self):
        self.manager.register_provider("p2", lambda: {})
        with self.assertRaises(DuplicateProviderError):
            self.manager.register_provider("p2", lambda: {})

    def test_broken_provider_raises_error(self):
        def bad_fn():
            raise ValueError("error")
        self.manager.register_provider("bad", bad_fn)
        with self.assertRaises(BrokenProviderError):
            self.manager.run_all()

    def test_plugin_inspector_checks(self):
        reg = PluginRegistry()
        reg.register_plugin(MockGoodPlugin())
        
        # Test good plugin
        res = PluginInspector.inspect_plugins(reg)
        self.assertEqual(res["status"], "Healthy")
        self.assertEqual(res["total_plugins"], 1)
        self.assertEqual(len(res["broken_plugins"]), 0)
        
        # Unregister and add bad plugin
        reg.unregister_plugin("good")
        
        class BadPluginStub(BasePlugin):
            def initialize(self) -> None: pass
            def execute(self, context: Dict[str, Any]) -> Any: pass
            def shutdown(self) -> None: pass
            def metadata(self) -> Dict[str, Any]:
                return {"id": "bad"}
                
        # Skip validate in registry to force add a bad plugin structure
        reg._plugins["bad"] = BadPluginStub()
        res_bad = PluginInspector.inspect_plugins(reg)
        self.assertEqual(res_bad["status"], "Critical")
        self.assertEqual(len(res_bad["broken_plugins"]), 1)

    def test_reporter_file_generation(self):
        # Register a provider in global manager for report test
        global_mgr = get_diagnostics_manager()
        global_mgr._providers.clear()
        global_mgr.register_provider("test_provider", lambda: {"status": "Good"})
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = DiagnosticsReporter.generate_report(workspace_root=tmp_dir)
            self.assertEqual(report["diagnostics"]["test_provider"]["status"], "Good")
            
            file_path = os.path.join(tmp_dir, "workflow_diagnostics.json")
            self.assertTrue(os.path.exists(file_path))
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["diagnostics"]["test_provider"]["status"], "Good")

if __name__ == "__main__":
    unittest.main()
