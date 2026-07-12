import unittest
import tempfile
import os
import json
from core.workflow.stage import WorkflowStage
from core.workflow.pipeline import Pipeline
from core.workflow.workflow import WorkflowOrchestrator
from core.workflow.state import StageStatus, WorkflowStatus
from core.workflow.exceptions import (
    DuplicateStageError,
    CircularDependencyError,
    ValidationError,
    MissingArtifactError
)
from core.artifacts.registry import ArtifactRegistry

class TestWorkflowOrchestrator(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.registry = ArtifactRegistry(self.temp_dir.name)
        self.orchestrator = WorkflowOrchestrator(self.registry)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_workflow_creation_and_stage_ordering(self):
        pipeline = Pipeline("Test Pipeline")
        s2 = WorkflowStage(
            stage_id="stage2",
            stage_name="Stage 2",
            engine_name="Language Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson_language.json"],
            dependencies=["stage1"]
        )
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s2)
        pipeline.add_stage(s1)
        
        order = self.orchestrator.scheduler.get_execution_order(pipeline.stages)
        self.assertEqual(order[0].stage_id, "stage1")
        self.assertEqual(order[1].stage_id, "stage2")

    async def test_scheduler_success_execution(self):
        pipeline = Pipeline("Test Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)

        def mock_execute(stage):
            pass

        execution = await self.orchestrator.start(pipeline, mock_execute)
        self.assertEqual(execution.status, WorkflowStatus.COMPLETED)
        self.assertEqual(execution.stages[0].status, StageStatus.COMPLETED)
        self.assertIn("lesson.json", execution.artifacts)

    async def test_scheduler_retry_and_fail(self):
        pipeline = Pipeline("Test Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)

        call_count = 0
        def mock_execute_fail(stage):
            nonlocal call_count
            call_count += 1
            raise ValueError("Failure simulation")

        execution = await self.orchestrator.start(pipeline, mock_execute_fail)
        self.assertEqual(execution.status, WorkflowStatus.FAILED)
        self.assertEqual(execution.stages[0].status, StageStatus.FAILED)
        self.assertEqual(call_count, 4)
        self.assertEqual(len(execution.stages[0].errors), 4)

    async def test_scheduler_retry_and_eventual_success(self):
        pipeline = Pipeline("Test Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)

        call_count = 0
        def mock_execute_eventual(stage):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Retry simulation")

        execution = await self.orchestrator.start(pipeline, mock_execute_eventual)
        self.assertEqual(execution.status, WorkflowStatus.COMPLETED)
        self.assertEqual(execution.stages[0].status, StageStatus.COMPLETED)
        self.assertEqual(call_count, 3)

    async def test_scheduler_resume_skips_completed(self):
        pipeline = Pipeline("Test Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        s2 = WorkflowStage(
            stage_id="stage2",
            stage_name="Stage 2",
            engine_name="Language Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson_language.json"],
            dependencies=["stage1"]
        )
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)

        s1_executed = False
        def mock_execute(stage):
            nonlocal s1_executed
            if stage.stage_id == "stage1":
                s1_executed = True

        execution = await self.orchestrator.start(pipeline, mock_execute)
        self.assertTrue(s1_executed)
        
        execution.stages[0].status = StageStatus.COMPLETED
        execution.stages[1].status = StageStatus.PENDING
        s1_executed = False
        
        await self.orchestrator.resume(execution, mock_execute)
        self.assertFalse(s1_executed)
        self.assertEqual(execution.stages[0].status, StageStatus.SKIPPED)
        self.assertEqual(execution.stages[1].status, StageStatus.COMPLETED)

    async def test_scheduler_restart_runs_all(self):
        pipeline = Pipeline("Test Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)

        def mock_execute(stage):
            pass

        execution = await self.orchestrator.start(pipeline, mock_execute)
        self.assertEqual(execution.stages[0].status, StageStatus.COMPLETED)

        re_execution = await self.orchestrator.restart(execution, mock_execute)
        self.assertEqual(re_execution.stages[0].status, StageStatus.COMPLETED)

    def test_validation_duplicate_stages(self):
        pipeline = Pipeline("Dup Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        s2 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 2",
            engine_name="Language Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson_language.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)
        with self.assertRaises(DuplicateStageError):
            self.orchestrator.validate(pipeline)

    def test_validation_circular_dependencies(self):
        pipeline = Pipeline("Cycle Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=["stage2"]
        )
        s2 = WorkflowStage(
            stage_id="stage2",
            stage_name="Stage 2",
            engine_name="Language Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson_language.json"],
            dependencies=["stage1"]
        )
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)
        with self.assertRaises(CircularDependencyError):
            self.orchestrator.validate(pipeline)

    def test_validation_missing_input_artifacts(self):
        pipeline = Pipeline("Missing Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["missing_input.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)
        with self.assertRaises(MissingArtifactError):
            self.orchestrator.validate(pipeline)

    def test_validation_orphan_stage(self):
        pipeline = Pipeline("Orphan Pipeline")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        s2 = WorkflowStage(
            stage_id="stage2",
            stage_name="Stage 2",
            engine_name="Language Intelligence Engine",
            inputs=[],
            outputs=["some_out.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)
        with self.assertRaises(ValidationError):
            self.orchestrator.validate(pipeline)

    async def test_workflow_history_and_serialization(self):
        pipeline = Pipeline("Test History")
        s1 = WorkflowStage(
            stage_id="stage1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["lesson.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)
        
        execution = await self.orchestrator.start(pipeline, lambda x: None)
        
        self.assertEqual(len(self.orchestrator.history()), 1)
        
        target_path = os.path.join(self.temp_dir.name, "workflow_execution.json")
        self.assertTrue(os.path.exists(target_path))
        with open(target_path, "r") as f:
            data = json.load(f)
            self.assertEqual(data["workflow_id"], execution.workflow_id)
            self.assertEqual(data["status"], "COMPLETED")

if __name__ == "__main__":
    unittest.main()
