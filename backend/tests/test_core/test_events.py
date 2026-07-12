import unittest
import datetime
import uuid
from core.events.event import Event
from core.events.dispatcher import EventDispatcher
from core.workflow.stage import WorkflowStage
from core.workflow.pipeline import Pipeline
from core.workflow.workflow import WorkflowOrchestrator
from core.artifacts.registry import ArtifactRegistry, get_canonical_registry

class TestEventBus(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.dispatcher = EventDispatcher()
        self.events_received = []

    def log_event(self, event: Event):
        self.events_received.append(event)

    def test_event_publication_and_subscription(self):
        self.dispatcher.subscribe("TestEvent", self.log_event)
        
        evt = Event(
            event_id="evt-1",
            event_name="TestEvent",
            source_engine="TestEngine",
            timestamp=datetime.datetime.now().isoformat(),
            payload={"key": "value"}
        )
        self.dispatcher.publish(evt)
        self.assertEqual(len(self.events_received), 1)
        self.assertEqual(self.events_received[0].payload["key"], "value")

    def test_unsubscribe(self):
        self.dispatcher.subscribe("TestEvent", self.log_event)
        self.dispatcher.unsubscribe("TestEvent", self.log_event)
        
        evt = Event(
            event_id="evt-1",
            event_name="TestEvent",
            source_engine="TestEngine",
            timestamp=datetime.datetime.now().isoformat()
        )
        self.dispatcher.publish(evt)
        self.assertEqual(len(self.events_received), 0)

    def test_wildcard_subscription(self):
        self.dispatcher.subscribe("*", self.log_event)
        
        evt1 = Event(
            event_id="evt-1",
            event_name="AnyEvent",
            source_engine="TestEngine",
            timestamp=datetime.datetime.now().isoformat()
        )
        evt2 = Event(
            event_id="evt-2",
            event_name="AnotherEvent",
            source_engine="TestEngine",
            timestamp=datetime.datetime.now().isoformat()
        )
        self.dispatcher.publish(evt1)
        self.dispatcher.publish(evt2)
        self.assertEqual(len(self.events_received), 2)

    def test_dispatch_order_history(self):
        self.dispatcher.subscribe("E1", self.log_event)
        self.dispatcher.subscribe("E2", self.log_event)
        
        evt1 = Event(
            event_id="evt-1",
            event_name="E1",
            source_engine="TestEngine",
            timestamp=datetime.datetime.now().isoformat()
        )
        evt2 = Event(
            event_id="evt-2",
            event_name="E2",
            source_engine="TestEngine",
            timestamp=datetime.datetime.now().isoformat()
        )
        self.dispatcher.publish(evt1)
        self.dispatcher.publish(evt2)
        
        history = self.dispatcher.history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].event_name, "E1")
        self.assertEqual(history[1].event_name, "E2")

    async def test_workflow_event_emission(self):
        # We will use the global dispatcher for the orchestrator, so we subscribe to it
        from core.events.dispatcher import get_event_dispatcher
        global_dispatcher = get_event_dispatcher()
        
        received_global = []
        global_dispatcher.subscribe("WorkflowStarted", received_global.append)
        global_dispatcher.subscribe("WorkflowCompleted", received_global.append)
        global_dispatcher.subscribe("StageStarted", received_global.append)
        global_dispatcher.subscribe("StageCompleted", received_global.append)
        global_dispatcher.subscribe("ArtifactProduced", received_global.append)
        
        pipeline = Pipeline("Standard Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)
        
        orchestrator = WorkflowOrchestrator()
        await orchestrator.start(pipeline, lambda x: None)
        
        # Verify that all standard pipeline events were published
        names = [evt.event_name for evt in received_global]
        self.assertIn("WorkflowStarted", names)
        self.assertIn("WorkflowCompleted", names)
        self.assertIn("StageStarted", names)
        self.assertIn("StageCompleted", names)
        self.assertIn("ArtifactProduced", names)

    def test_artifact_validated_event(self):
        from core.events.dispatcher import get_event_dispatcher
        global_dispatcher = get_event_dispatcher()
        
        received = []
        global_dispatcher.subscribe("ArtifactValidated", received.append)
        
        registry = get_canonical_registry()
        registry.validate("lesson.json")
        
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].event_name, "ArtifactValidated")
        self.assertEqual(received[0].payload["artifact_id"], "lesson.json")

if __name__ == "__main__":
    unittest.main()
