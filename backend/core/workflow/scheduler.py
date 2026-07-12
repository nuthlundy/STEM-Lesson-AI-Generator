import time
import inspect
from typing import List, Dict, Set, Callable, Any
from core.workflow.stage import WorkflowStage
from core.workflow.state import StageStatus, WorkflowStatus
from core.workflow.validator import WorkflowValidator
from core.workflow.exceptions import CircularDependencyError

class WorkflowScheduler:
    """Orchestrates stage dependency sorting, retries, and sequential execution."""
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def get_execution_order(self, stages: List[WorkflowStage]) -> List[WorkflowStage]:
        """Calculates correct execution order using topological sorting on stage dependencies."""
        WorkflowValidator.validate_pipeline(stages)
        
        adj: Dict[str, Set[str]] = {s.stage_id: set(s.dependencies) for s in stages}
        visited: Set[str] = set()
        stack: List[str] = []

        def dfs(node: str) -> None:
            visited.add(node)
            for dep in adj.get(node, []):
                if dep in adj and dep not in visited:
                    dfs(dep)
            stack.append(node)

        for s in sorted(stages, key=lambda x: x.stage_id):
            if s.stage_id not in visited:
                dfs(s.stage_id)

        stage_map = {s.stage_id: s for s in stages}
        return [stage_map[sid] for sid in stack]

    async def execute_sequentially(
        self,
        stages: List[WorkflowStage],
        execute_fn: Callable[[WorkflowStage], Any],
        workflow_id: str = None
    ) -> WorkflowStatus:
        from core.events.event import Event
        from core.events.dispatcher import get_event_dispatcher
        import datetime
        import uuid
        
        dispatcher = get_event_dispatcher()
        ordered_stages = self.get_execution_order(stages)
        stage_status_map = {s.stage_id: s.status for s in stages}
        
        for stage in ordered_stages:
            if stage_status_map[stage.stage_id] == StageStatus.COMPLETED:
                stage.status = StageStatus.SKIPPED
                continue
                
            ready = True
            for dep in stage.dependencies:
                if stage_status_map.get(dep) not in (StageStatus.COMPLETED, StageStatus.SKIPPED):
                    ready = False
                    break
                    
            if not ready:
                stage.status = StageStatus.FAILED
                stage.errors.append("Dependencies not met.")
                stage_status_map[stage.stage_id] = StageStatus.FAILED
                
                dispatcher.publish(Event(
                    event_id=str(uuid.uuid4()),
                    event_name="StageFailed",
                    source_engine=stage.engine_name,
                    workflow_id=workflow_id,
                    timestamp=datetime.datetime.now().isoformat(),
                    payload={"stage_id": stage.stage_id, "error": "Dependencies not met."}
                ))
                return WorkflowStatus.FAILED
                
            stage.status = StageStatus.RUNNING
            dispatcher.publish(Event(
                event_id=str(uuid.uuid4()),
                event_name="StageStarted",
                source_engine=stage.engine_name,
                workflow_id=workflow_id,
                timestamp=datetime.datetime.now().isoformat(),
                payload={"stage_id": stage.stage_id}
            ))
            
            from core.logging.context import get_logging_context
            from core.monitoring.tracker import get_metrics_tracker
            from core.monitoring.profiler import Profiler
            
            profiler = Profiler()
            retries = 0
            success = False
            
            with profiler:
                while retries <= self.max_retries:
                    try:
                        if inspect.iscoroutinefunction(execute_fn):
                            await execute_fn(stage)
                        else:
                            execute_fn(stage)
                        success = True
                        break
                    except Exception as e:
                        retries += 1
                        stage.errors.append(f"Retry {retries} failed: {e}")
                        
            stage.execution_time = profiler.duration
            
            try:
                ctx = get_logging_context()
                p_name = ctx.get("pipeline_id")
                if p_name:
                    get_metrics_tracker().record_stage_execution(
                        pipeline_name=p_name,
                        stage_id=stage.stage_id,
                        duration=profiler.duration,
                        memory_usage=profiler.peak_memory,
                        success=success,
                        retries=retries
                    )
            except Exception:
                pass
            
            if success:
                stage.status = StageStatus.COMPLETED
                stage_status_map[stage.stage_id] = StageStatus.COMPLETED
                
                dispatcher.publish(Event(
                    event_id=str(uuid.uuid4()),
                    event_name="StageCompleted",
                    source_engine=stage.engine_name,
                    workflow_id=workflow_id,
                    timestamp=datetime.datetime.now().isoformat(),
                    payload={"stage_id": stage.stage_id, "execution_time": stage.execution_time}
                ))
                
                # Publish ArtifactProduced events
                for out in stage.outputs:
                    dispatcher.publish(Event(
                        event_id=str(uuid.uuid4()),
                        event_name="ArtifactProduced",
                        source_engine=stage.engine_name,
                        workflow_id=workflow_id,
                        timestamp=datetime.datetime.now().isoformat(),
                        payload={"artifact_id": out, "stage_id": stage.stage_id}
                    ))
            else:
                stage.status = StageStatus.FAILED
                stage_status_map[stage.stage_id] = StageStatus.FAILED
                
                dispatcher.publish(Event(
                    event_id=str(uuid.uuid4()),
                    event_name="StageFailed",
                    source_engine=stage.engine_name,
                    workflow_id=workflow_id,
                    timestamp=datetime.datetime.now().isoformat(),
                    payload={"stage_id": stage.stage_id, "errors": stage.errors}
                ))
                return WorkflowStatus.FAILED
                
        return WorkflowStatus.COMPLETED
