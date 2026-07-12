class WorkflowError(Exception):
    """Base exception for all Workflow Orchestration errors."""
    pass

class DuplicateStageError(WorkflowError):
    """Raised when adding a stage with a duplicate ID."""
    pass

class StageNotFoundError(WorkflowError):
    """Raised when requesting a stage that doesn't exist."""
    pass

class ValidationError(WorkflowError):
    """Raised when validation of stage/pipeline dependencies fails."""
    pass

class CircularDependencyError(WorkflowError):
    """Raised when circular dependency is detected among stages."""
    pass

class MissingArtifactError(WorkflowError):
    """Raised when a required artifact is missing or not registered."""
    pass
