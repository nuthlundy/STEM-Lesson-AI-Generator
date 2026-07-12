class MonitoringError(Exception):
    """Base exception for all monitoring errors."""
    pass

class DuplicateMetricError(MonitoringError):
    """Raised when registering a metric that already exists."""
    pass

class MissingCollectorError(MonitoringError):
    """Raised when a required metric collector is missing."""
    pass
