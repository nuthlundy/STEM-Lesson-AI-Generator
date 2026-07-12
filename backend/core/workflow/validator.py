from typing import List, Dict, Set
from core.workflow.stage import WorkflowStage
from core.workflow.exceptions import (
    DuplicateStageError,
    CircularDependencyError,
    ValidationError,
    MissingArtifactError
)

class WorkflowValidator:
    """Validates pipeline execution structures, duplicate stages, and cyclic dependencies."""
    
    @staticmethod
    def validate_pipeline(stages: List[WorkflowStage]) -> None:
        seen_stage_ids = set()
        for s in stages:
            if s.stage_id in seen_stage_ids:
                raise DuplicateStageError(f"Duplicate stage ID: '{s.stage_id}'")
            seen_stage_ids.add(s.stage_id)
            
        adj: Dict[str, Set[str]] = {s.stage_id: set(s.dependencies) for s in stages}
        
        for sid, deps in adj.items():
            for dep in deps:
                if dep not in adj:
                    raise ValidationError(f"Stage '{sid}' depends on missing stage '{dep}'.")
                    
        visited = {sid: 0 for sid in adj}
        
        def dfs(node: str) -> bool:
            visited[node] = 1
            for dep in adj[node]:
                if visited[dep] == 1:
                    return True
                if visited[dep] == 0:
                    if dfs(dep):
                        return True
            visited[node] = 2
            return False

        for sid in adj:
            if visited[sid] == 0:
                if dfs(sid):
                    raise CircularDependencyError(f"Circular dependency detected involving stage: '{sid}'")
                    
        produced_artifacts = set()
        for s in stages:
            for out in s.outputs:
                produced_artifacts.add(out)
                
        for s in stages:
            for inp in s.inputs:
                if inp not in produced_artifacts and inp != "lesson.json":
                    raise MissingArtifactError(f"Stage '{s.stage_id}' requires missing input artifact: '{inp}'")

        if len(stages) > 1:
            for s in stages:
                has_dep = len(s.dependencies) > 0
                has_consumers = any(s.stage_id in other.dependencies for other in stages if other.stage_id != s.stage_id)
                has_io_link = False
                for other in stages:
                    if other.stage_id == s.stage_id:
                        continue
                    if any(inp in s.outputs for inp in other.inputs):
                        has_io_link = True
                    if any(out in s.inputs for out in other.outputs):
                        has_io_link = True
                
                if not has_dep and not has_consumers and not has_io_link:
                    raise ValidationError(f"Orphan stage detected: '{s.stage_id}' is isolated from the pipeline.")
