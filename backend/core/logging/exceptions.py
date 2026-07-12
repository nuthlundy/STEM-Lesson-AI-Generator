class LoggingError(Exception):
    """Base exception for all logging errors."""
    pass

class InvalidHandlerError(LoggingError):
    """Raised when duplicate or invalid handlers are registered."""
    pass

class InvalidLogLevelError(LoggingError):
    """Raised when an invalid log level is requested."""
    pass
