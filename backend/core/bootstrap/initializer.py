from core.logging.factory import LoggerFactory
from core.events.dispatcher import get_event_dispatcher
from core.plugins.registry import PluginRegistry
from core.plugins.manager import PluginManager
from core.workflow.workflow import WorkflowOrchestrator
from core.artifacts.registry import get_canonical_registry

class PlatformInitializer:
    @staticmethod
    def initialize() -> dict:
        logger = LoggerFactory.get_logger("Platform", "INFO")
        logger.info("Initializing core platform systems...")
        
        dispatcher = get_event_dispatcher()
        
        plugin_registry = PluginRegistry()
        plugin_manager = PluginManager(plugin_registry)
        
        artifact_registry = get_canonical_registry()
        
        orchestrator = WorkflowOrchestrator(artifact_registry)
        
        logger.info("Core platform systems initialized successfully.")
        
        return {
            "logger": logger,
            "dispatcher": dispatcher,
            "plugin_manager": plugin_manager,
            "artifact_registry": artifact_registry,
            "orchestrator": orchestrator
        }
