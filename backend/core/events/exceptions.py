class EventError(Exception):
    """Base exception for all Event Bus errors."""
    pass

class InvalidEventError(EventError):
    """Raised when an event does not conform to validation schemas."""
    pass
