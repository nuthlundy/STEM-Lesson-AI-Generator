class ConfigurationError(Exception):
    """Base exception for all Configuration errors."""
    pass

class ValidationError(ConfigurationError):
    """Raised when configuration variables or environments are invalid."""
    pass

class ProviderError(ConfigurationError):
    """Base exception for all Provider registry errors."""
    pass

class DuplicateProviderError(ProviderError):
    """Raised when registering an AI provider that is already registered."""
    pass

class ProviderNotFoundError(ProviderError):
    """Raised when requesting an unregistered AI provider."""
    pass

class InvalidEnvironmentError(ConfigurationError):
    """Raised when environment name is not recognized."""
    pass
