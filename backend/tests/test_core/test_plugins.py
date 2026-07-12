import unittest
from typing import Dict, Any
from core.plugins.plugin import BasePlugin
from core.plugins.interfaces import (
    AIProviderPlugin,
    RenderingPlugin,
    LmsExportPlugin,
    AssessmentPlugin
)
from core.plugins.registry import PluginRegistry
from core.plugins.loader import PluginLoader
from core.plugins.manager import PluginManager
from core.plugins.exceptions import (
    DuplicatePluginError,
    PluginNotFoundError,
    InvalidPluginError
)

class MockAIPlugin(AIProviderPlugin):
    def __init__(self):
        self.initialized = False
        self.shutdown_called = False

    def initialize(self) -> None:
        self.initialized = True

    def execute(self, context: Dict[str, Any]) -> Any:
        return "executed"

    def shutdown(self) -> None:
        self.shutdown_called = True

    def metadata(self) -> Dict[str, Any]:
        return {
            "id": "mock-ai-provider",
            "name": "Mock AI Provider",
            "version": "1.0.0",
            "type": "AIProvider"
        }

    def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        return f"Response to: {prompt}"

class MockRenderingPlugin(RenderingPlugin):
    def initialize(self) -> None:
        pass
    def execute(self, context: Dict[str, Any]) -> Any:
        pass
    def shutdown(self) -> None:
        pass
    def metadata(self) -> Dict[str, Any]:
        return {"id": "mock-render", "name": "Mock Render", "version": "1.0.0", "type": "Rendering"}
    def render(self, lesson_plan_data: Dict[str, Any], output_format: str) -> bytes:
        return b"rendered_output"

class MockLmsPlugin(LmsExportPlugin):
    def initialize(self) -> None:
        pass
    def execute(self, context: Dict[str, Any]) -> Any:
        pass
    def shutdown(self) -> None:
        pass
    def metadata(self) -> Dict[str, Any]:
        return {"id": "mock-lms", "name": "Mock LMS", "version": "1.0.0", "type": "LmsExport"}
    def export_to_lms(self, lesson_plan_data: Dict[str, Any], target_lms: str) -> bool:
        return True

class MockAssessmentPlugin(AssessmentPlugin):
    def initialize(self) -> None:
        pass
    def execute(self, context: Dict[str, Any]) -> Any:
        pass
    def shutdown(self) -> None:
        pass
    def metadata(self) -> Dict[str, Any]:
        return {"id": "mock-assessment", "name": "Mock Assessment", "version": "1.0.0", "type": "Assessment"}
    def generate_rubric(self, learning_objectives: list) -> Dict[str, Any]:
        return {"rubric": "rubric_data"}

class TestPluginSystem(unittest.TestCase):
    def setUp(self):
        self.registry = PluginRegistry()

    def test_plugin_metadata(self):
        plugin = MockAIPlugin()
        meta = plugin.metadata()
        self.assertEqual(meta["id"], "mock-ai-provider")
        self.assertEqual(meta["type"], "AIProvider")

    def test_plugin_registration_success(self):
        plugin = MockAIPlugin()
        self.registry.register_plugin(plugin)
        self.assertEqual(self.registry.get_plugin("mock-ai-provider"), plugin)
        self.assertIn(plugin, self.registry.list_plugins())

    def test_plugin_duplicate_registration(self):
        plugin = MockAIPlugin()
        self.registry.register_plugin(plugin)
        with self.assertRaises(DuplicatePluginError):
            self.registry.register_plugin(plugin)

    def test_plugin_not_found(self):
        with self.assertRaises(PluginNotFoundError):
            self.registry.get_plugin("non-existent-plugin")

    def test_plugin_unregister(self):
        plugin = MockAIPlugin()
        self.registry.register_plugin(plugin)
        self.registry.unregister_plugin("mock-ai-provider")
        with self.assertRaises(PluginNotFoundError):
            self.registry.get_plugin("mock-ai-provider")

    def test_plugin_validation_invalid_class(self):
        class NotAPlugin:
            pass
        with self.assertRaises(InvalidPluginError):
            self.registry.register_plugin(NotAPlugin())

    def test_plugin_validation_missing_metadata_keys(self):
        class BadPlugin(BasePlugin):
            def initialize(self) -> None: pass
            def execute(self, context: Dict[str, Any]) -> Any: pass
            def shutdown(self) -> None: pass
            def metadata(self) -> Dict[str, Any]:
                return {"id": "bad"} # missing name, version, type
        with self.assertRaises(InvalidPluginError):
            self.registry.register_plugin(BadPlugin())

    def test_plugin_loader(self):
        plugin = PluginLoader.load_plugin(MockAIPlugin)
        self.assertIsInstance(plugin, MockAIPlugin)

    def test_plugin_manager_lifecycle(self):
        plugin = MockAIPlugin()
        self.registry.register_plugin(plugin)
        manager = PluginManager(self.registry)
        
        manager.initialize_all()
        self.assertTrue(plugin.initialized)
        
        result = manager.execute_plugin("mock-ai-provider", {})
        self.assertEqual(result, "executed")
        
        manager.shutdown_all()
        self.assertTrue(plugin.shutdown_called)

    def test_ai_provider_plugin_interface(self):
        plugin = MockAIPlugin()
        self.registry.register_plugin(plugin)
        text = plugin.generate_text("Hello")
        self.assertEqual(text, "Response to: Hello")

    def test_rendering_plugin_interface(self):
        plugin = MockRenderingPlugin()
        self.registry.register_plugin(plugin)
        output = plugin.render({}, "pdf")
        self.assertEqual(output, b"rendered_output")

    def test_lms_export_plugin_interface(self):
        plugin = MockLmsPlugin()
        self.registry.register_plugin(plugin)
        success = plugin.export_to_lms({}, "canvas")
        self.assertTrue(success)

    def test_assessment_plugin_interface(self):
        plugin = MockAssessmentPlugin()
        self.registry.register_plugin(plugin)
        rubric = plugin.generate_rubric([])
        self.assertEqual(rubric, {"rubric": "rubric_data"})

if __name__ == "__main__":
    unittest.main()
