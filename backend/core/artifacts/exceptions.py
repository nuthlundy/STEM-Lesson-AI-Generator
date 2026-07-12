class ArtifactRegistryError(Exception):
    """Base exception for all Artifact Registry errors."""
    pass

class DuplicateArtifactError(ArtifactRegistryError):
    """Raised when registering an artifact that is already registered."""
    pass

class ArtifactNotFoundError(ArtifactRegistryError):
    """Raised when requesting an unregistered artifact."""
    pass

class ValidationError(ArtifactRegistryError):
    """Raised when an artifact fails registry validation rules."""
    pass

class DependencyCycleError(ArtifactRegistryError):
    """Raised when a dependency cycle is detected among registered artifacts."""
    pass

class MissingDependencyError(ArtifactRegistryError):
    """Raised when an artifact depends on a missing/unregistered artifact."""
    pass
