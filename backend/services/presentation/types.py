class PresentationError(Exception):
    """Base exception for presentation engine."""
    pass

class SessionCreationError(PresentationError):
    """Raised when a presentation session cannot be created."""
    pass

class PresentationNotFoundError(PresentationError):
    """Raised when the target presentation file is not found."""
    pass
