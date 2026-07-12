class RenderingError(Exception):
    """Base exception for rendering engine."""
    pass

class UnsupportedFormatError(RenderingError):
    """Raised when rendering to an unsupported format."""
    pass

class LayoutError(RenderingError):
    """Raised when layout building fails."""
    pass
