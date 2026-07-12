class SubjectIntelligenceError(Exception):
    """Base exception for Subject Intelligence Engine."""
    pass

class ValidationFailedError(SubjectIntelligenceError):
    """Raised when formula or citation validation checks fail."""
    pass

class ProcessorConfigurationError(SubjectIntelligenceError):
    """Raised when processor initialization parameters are invalid or config is incorrect."""
    pass
