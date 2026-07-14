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
from core.config.settings import Settings
from core.config.providers import Provider
from core.config.validator import ConfigValidator
from core.config.exceptions import ValidationError as ConfigValidationError
from core.artifacts.registry import ArtifactRegistry
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

    # Milestone 2 New Regression and QA Tests
    def test_diagnostics_reporter_validation_coverage(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = DiagnosticsReporter.generate_report(workspace_root=tmp_dir)
            self.assertIn("validation_coverage", report)
            self.assertEqual(report["validation_coverage"]["Core Platform"], "Verified")

    def test_diagnostics_reporter_module_verification(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = DiagnosticsReporter.generate_report(workspace_root=tmp_dir)
            self.assertIn("module_verification", report)
            self.assertIn("WorkspaceEngine", report["module_verification"])

    def test_diagnostics_reporter_regression_summary(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = DiagnosticsReporter.generate_report(workspace_root=tmp_dir)
            self.assertIn("regression_summary", report)
            self.assertEqual(report["regression_summary"]["total_target_tests"], 750)

    def test_diagnostics_reporter_execution_consistency(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            report = DiagnosticsReporter.generate_report(workspace_root=tmp_dir)
            self.assertIn("execution_consistency", report)
            self.assertEqual(report["execution_consistency"]["sequence_status"], "consistent")

    def test_config_validator_directory_checks_invalid(self):
        # We set an invalid directory that cannot be created (e.g. invalid character or null byte)
        settings = Settings(
            workspace="\0invalid_dir",
            environment="production",
            retry_policy=3,
            timeout=30.0
        )
        with self.assertRaises(ConfigValidationError):
            ConfigValidator.validate_settings(settings)

    def test_config_validator_dependency_checks_pass(self):
        # Normal settings validation should pass dependencies check
        with tempfile.TemporaryDirectory() as tmp_dir:
            settings = Settings(
                workspace=tmp_dir,
                environment="testing",
                retry_policy=5,
                timeout=10.0
            )
            ConfigValidator.validate_settings(settings) # Should not raise


    def test_config_validator_environment_checks_invalid(self):
        settings = Settings(
            environment="invalid_env",
            retry_policy=3,
            timeout=30.0
        )
        with self.assertRaises(ConfigValidationError):
            ConfigValidator.validate_settings(settings)

    def test_config_validator_retry_policy_checks_invalid(self):
        settings = Settings(
            environment="development",
            retry_policy=11, # Out of 0-10 bounds
            timeout=30.0
        )
        with self.assertRaises(ConfigValidationError):
            ConfigValidator.validate_settings(settings)

    def test_config_validator_timeout_checks_invalid(self):
        settings = Settings(
            environment="development",
            retry_policy=5,
            timeout=0.0 # Timeout <= 0
        )
        with self.assertRaises(ConfigValidationError):
            ConfigValidator.validate_settings(settings)

    def test_config_validator_provider_invalid_type(self):
        prov = Provider(
            provider_name="TestProv",
            provider_type="InvalidType",
            model_name="gpt-4"
        )
        with self.assertRaises(ConfigValidationError):
            ConfigValidator.validate_provider(prov)

    def test_config_validator_provider_empty_name(self):
        prov = Provider(
            provider_name="  ",
            provider_type="Gemini",
            model_name="gemini-1.5-pro"
        )
        with self.assertRaises(ConfigValidationError):
            ConfigValidator.validate_provider(prov)

    def test_config_validator_provider_empty_model(self):
        prov = Provider(
            provider_name="MyProv",
            provider_type="Claude",
            model_name=""
        )
        with self.assertRaises(ConfigValidationError):
            ConfigValidator.validate_provider(prov)

    def test_diagnostics_validator_config_checks(self):
        from core.config.registry import ConfigRegistry
        reg = ConfigRegistry()
        res = DiagnosticsValidator.validate_config(reg)
        self.assertEqual(res["status"], "Healthy")

    def test_diagnostics_validator_artifacts_checks(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            reg = ArtifactRegistry(tmp_dir)
            res = DiagnosticsValidator.validate_artifacts(reg)
            self.assertEqual(res["status"], "Healthy")

    def test_diagnostics_inspector_plugins_handles_exception(self):
        reg = PluginRegistry()
        class ExplodingPlugin(BasePlugin):
            def initialize(self) -> None: pass
            def execute(self, context: Dict[str, Any]) -> Any: pass
            def shutdown(self) -> None: pass
            def metadata(self) -> Dict[str, Any]:
                raise RuntimeError("Boom")
        reg._plugins["explode"] = ExplodingPlugin()
        res = PluginInspector.inspect_plugins(reg)
        self.assertEqual(res["status"], "Critical")
        self.assertEqual(len(res["broken_plugins"]), 1)
        self.assertIn("Boom", res["broken_plugins"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
