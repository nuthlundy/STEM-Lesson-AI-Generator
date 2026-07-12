class DiagnosticsError(Exception):
    """Base exception for diagnostics framework."""
    pass

class DuplicateProviderError(DiagnosticsError):
    """Raised when registering duplicate diagnostics providers."""
    pass

class BrokenProviderError(DiagnosticsError):
    """Raised when a diagnostic provider fails execution or returns invalid results."""
    pass
