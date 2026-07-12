import datetime
import uuid
import json
import os
from typing import List, Dict, Any, Callable
from core.workflow.pipeline import Pipeline
from core.workflow.stage import WorkflowStage
from core.workflow.execution import WorkflowExecution
from core.workflow.state import WorkflowStatus, StageStatus
from core.workflow.scheduler import WorkflowScheduler
from core.workflow.validator import WorkflowValidator
from core.artifacts.registry import ArtifactRegistry, get_canonical_registry

class WorkflowOrchestrator:
    """Manages workflow runs, history, state changes, and writes workflow_execution.json."""
    
    def __init__(self, registry: ArtifactRegistry = None):
        self.registry = registry if registry else get_canonical_registry()
        self.scheduler = WorkflowScheduler()
        self.run_history: List[WorkflowExecution] = []

    def validate(self, pipeline: Pipeline) -> None:
        """Validates pipeline structure for cycles, duplicates, and missing inputs."""
        WorkflowValidator.validate_pipeline(pipeline.stages)

    async def start(
        self,
        pipeline: Pipeline,
        execute_fn: Callable[[WorkflowStage], Any]
    ) -> WorkflowExecution:
        """Starts a new pipeline run."""
        self.validate(pipeline)
        
        execution = WorkflowExecution(
            workflow_id=str(uuid.uuid4()),
            pipeline_name=pipeline.name,
            stages=[WorkflowStage(**s.model_dump()) for s in pipeline.stages],
            started_at=datetime.datetime.now().isoformat(),
            status=WorkflowStatus.RUNNING
        )
        self.run_history.append(execution)
        
        return await self._run_execution(execution, execute_fn)

    async def resume(
        self,
        execution: WorkflowExecution,
        execute_fn: Callable[[WorkflowStage], Any]
    ) -> WorkflowExecution:
        """Resumes a failed or stopped execution, skipping completed stages."""
        execution.status = WorkflowStatus.RUNNING
        execution.finished_at = None
        
        return await self._run_execution(execution, execute_fn)

    async def restart(
        self,
        execution: WorkflowExecution,
        execute_fn: Callable[[WorkflowStage], Any]
    ) -> WorkflowExecution:
        """Restarts an execution from scratch by resetting all stage statuses to PENDING."""
        for s in execution.stages:
            s.status = StageStatus.PENDING
            s.execution_time = 0.0
            s.errors = []
            
        execution.status = WorkflowStatus.RUNNING
        execution.finished_at = None
        execution.execution_time = 0.0
        
        return await self._run_execution(execution, execute_fn)

    def stop(self, execution: WorkflowExecution) -> WorkflowExecution:
        """Gracefully stops a running execution."""
        if execution.status == WorkflowStatus.RUNNING:
            execution.status = WorkflowStatus.STOPPED
            execution.finished_at = datetime.datetime.now().isoformat()
            
            for s in execution.stages:
                if s.status == StageStatus.RUNNING:
                    s.status = StageStatus.PENDING
                    s.errors.append("Execution stopped by user.")
                    
            self._save_execution_json(execution)
            
        return execution

    def status(self, execution: WorkflowExecution) -> WorkflowStatus:
        """Returns the current status of an execution."""
        return execution.status

    def history(self) -> List[WorkflowExecution]:
        """Returns the in-memory history of all executions run by this orchestrator."""
        return self.run_history

    async def _run_execution(
        self,
        execution: WorkflowExecution,
        execute_fn: Callable[[WorkflowStage], Any]
    ) -> WorkflowExecution:
        from core.events.event import Event
        from core.events.dispatcher import get_event_dispatcher
        dispatcher = get_event_dispatcher()
        
        dispatcher.publish(Event(
            event_id=str(uuid.uuid4()),
            event_name="WorkflowStarted",
            source_engine="WorkflowOrchestrator",
            workflow_id=execution.workflow_id,
            timestamp=datetime.datetime.now().isoformat(),
            payload={"pipeline_name": execution.pipeline_name}
        ))
        
        start_time = datetime.datetime.now()
        
        final_status = await self.scheduler.execute_sequentially(execution.stages, execute_fn, workflow_id=execution.workflow_id)
        
        execution.status = final_status
        execution.finished_at = datetime.datetime.now().isoformat()
        
        total_delta = datetime.datetime.fromisoformat(execution.finished_at) - start_time
        execution.execution_time = round(total_delta.total_seconds(), 3)
        
        generated = []
        for s in execution.stages:
            if s.status == StageStatus.COMPLETED or s.status == StageStatus.SKIPPED:
                for out in s.outputs:
                    if out not in generated:
                        generated.append(out)
        execution.artifacts = generated
        
        self._save_execution_json(execution)
        
        dispatcher.publish(Event(
            event_id=str(uuid.uuid4()),
            event_name="WorkflowCompleted",
            source_engine="WorkflowOrchestrator",
            workflow_id=execution.workflow_id,
            timestamp=datetime.datetime.now().isoformat(),
            payload={"pipeline_name": execution.pipeline_name, "status": final_status}
        ))
        
        return execution

    def _save_execution_json(self, execution: WorkflowExecution) -> None:
        """Saves workflow_execution.json in the registry absolute directory."""
        target_dir = self.registry._resolver.workspace_root
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, "workflow_execution.json")
        
        with open(file_path, "w") as f:
            json.dump(execution.model_dump(), f, indent=2)
