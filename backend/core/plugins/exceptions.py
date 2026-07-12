class PluginError(Exception):
    """Base exception for all Plugin-related errors."""
    pass

class DuplicatePluginError(PluginError):
    """Raised when registering a plugin with an ID that is already registered."""
    pass

class PluginNotFoundError(PluginError):
    """Raised when requesting an unregistered plugin."""
    pass

class InvalidPluginError(PluginError):
    """Raised when a plugin fails validation checks."""
    pass
