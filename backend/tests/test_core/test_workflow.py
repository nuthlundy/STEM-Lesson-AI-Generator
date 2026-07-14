import unittest
import tempfile
import os
import json
import fitz
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

    def create_valid_pdf(self, path: str):
        doc = fitz.open()
        page = doc.new_page(width=600, height=800)
        page.insert_text((50, 50), "Lesson Title: Newtonian gravity", fontsize=20)
        doc.save(path)
        doc.close()

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

    def test_topological_sort_independent_order(self):
        pipeline = Pipeline("Independent Pipeline")
        s1 = WorkflowStage(stage_id="s1", stage_name="S1", engine_name="E1", inputs=["lesson.json"], outputs=["lesson.json"])
        s2 = WorkflowStage(stage_id="s2", stage_name="S2", engine_name="E2", inputs=["lesson.json"], outputs=["lesson.json"])
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)
        order = self.orchestrator.scheduler.get_execution_order(pipeline.stages)
        self.assertEqual(len(order), 2)

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

    # Milestone 1 (Release Candidate) New Tests
    async def test_production_pipeline_orchestration_structure(self):
        mock_pdf = os.path.join(self.temp_dir.name, "test_input.pdf")
        self.create_valid_pdf(mock_pdf)
            
        execution = await self.orchestrator.run_production_pipeline(
            job_id="test-job-e2e",
            pdf_path=mock_pdf,
            workspace_root=self.temp_dir.name
        )
        self.assertEqual(execution.status, WorkflowStatus.COMPLETED)
        self.assertEqual(len(execution.stages), 11)

    async def test_production_pipeline_required_input_validation(self):
        # We run the production pipeline without faking the PDF, which should fail
        execution = await self.orchestrator.run_production_pipeline(
            job_id="test-job-e2e-fail",
            pdf_path=os.path.join(self.temp_dir.name, "missing.pdf"),
            workspace_root=self.temp_dir.name
        )
        self.assertEqual(execution.status, WorkflowStatus.FAILED)

    async def test_production_pipeline_diagnostics_produced(self):
        mock_pdf = os.path.join(self.temp_dir.name, "test_input.pdf")
        self.create_valid_pdf(mock_pdf)
            
        await self.orchestrator.run_production_pipeline(
            job_id="test-job-e2e-diag",
            pdf_path=mock_pdf,
            workspace_root=self.temp_dir.name
        )
        
        diag_path = os.path.join(self.temp_dir.name, "pipeline_diagnostics.json")
        self.assertTrue(os.path.exists(diag_path))
        with open(diag_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("stage_durations", data)
        self.assertIn("failed_stages", data)
        self.assertIn("recovered_stages", data)

    async def test_production_pipeline_partial_artifact_cleanup_on_error(self):
        # We inject a faked failed execute callback or stage
        pipeline = Pipeline("Failing Cleanup Pipeline")
        s1 = WorkflowStage(
            stage_id="s1",
            stage_name="Stage 1",
            engine_name="Document Intelligence Engine",
            inputs=["lesson.json"],
            outputs=["corrupt.json"],
            dependencies=[]
        )
        pipeline.add_stage(s1)
        
        # Write the corrupt artifact first to simulate partial write before fail
        corrupt_file = os.path.join(self.temp_dir.name, "corrupt.json")
        with open(corrupt_file, "w") as fh:
            fh.write("corrupt data")
            
        def mock_failing_execute(stage):
            raise RuntimeError("Stage failed midway")
            
        # Run fails and does not propagate out of start (it returns status=FAILED)
        execution = await self.orchestrator.start(pipeline, mock_failing_execute)
        self.assertEqual(execution.status, WorkflowStatus.FAILED)
            
        # Corrupt file should be removed by the clean up block
        self.assertFalse(os.path.exists(corrupt_file))

    async def test_production_pipeline_event_bus_delivery(self):
        mock_pdf = os.path.join(self.temp_dir.name, "test_input.pdf")
        self.create_valid_pdf(mock_pdf)
            
        from core.events.dispatcher import get_event_dispatcher
        dispatcher = get_event_dispatcher()
        events = []
        dispatcher.subscribe("StageStarted", events.append)
        dispatcher.subscribe("StageCompleted", events.append)
        
        await self.orchestrator.run_production_pipeline(
            job_id="test-job-events",
            pdf_path=mock_pdf,
            workspace_root=self.temp_dir.name
        )
        self.assertTrue(len(events) > 0)

    async def test_production_pipeline_topological_cycle_error(self):
        pipeline = Pipeline("Cycle Test")
        s1 = WorkflowStage(stage_id="s1", stage_name="S1", engine_name="E1", inputs=["lesson.json"], outputs=["lesson.json"], dependencies=["s2"])
        s2 = WorkflowStage(stage_id="s2", stage_name="S2", engine_name="E2", inputs=["lesson.json"], outputs=["lesson.json"], dependencies=["s1"])
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)
        with self.assertRaises(CircularDependencyError):
            await self.orchestrator.start(pipeline, lambda x: None)

    async def test_production_pipeline_topological_orphan_error(self):
        pipeline = Pipeline("Orphan Test")
        s1 = WorkflowStage(stage_id="s1", stage_name="S1", engine_name="E1", inputs=["lesson.json"], outputs=["lesson.json"])
        s2 = WorkflowStage(stage_id="s2", stage_name="S2", engine_name="E2", inputs=[], outputs=["some.json"])
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)
        with self.assertRaises(ValidationError):
            await self.orchestrator.start(pipeline, lambda x: None)

    async def test_production_pipeline_topological_duplicate_error(self):
        pipeline = Pipeline("Duplicate Test")
        s1 = WorkflowStage(stage_id="s1", stage_name="S1", engine_name="E1", inputs=["lesson.json"], outputs=["lesson.json"])
        s2 = WorkflowStage(stage_id="s1", stage_name="S2", engine_name="E2", inputs=["lesson.json"], outputs=["lesson.json"])
        pipeline.add_stage(s1)
        pipeline.add_stage(s2)
        with self.assertRaises(DuplicateStageError):
            await self.orchestrator.start(pipeline, lambda x: None)

if __name__ == "__main__":
    unittest.main()
