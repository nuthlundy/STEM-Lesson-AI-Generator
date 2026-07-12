from core.config.settings import Settings
from core.config.providers import Provider
from core.config.environments import Environment
from core.config.exceptions import ValidationError

VALID_PROVIDER_TYPES = {"Gemini", "OpenAI", "Claude", "Local LLM"}

class ConfigValidator:
    """Validates configuration parameters, retry policies, environment names, and timeout values."""
    
    @staticmethod
    def validate_settings(settings: Settings) -> None:
        valid_envs = {e.value for e in Environment}
        if settings.environment not in valid_envs:
            raise ValidationError(
                f"Invalid environment name: '{settings.environment}'. Must be one of {valid_envs}."
            )
            
        if settings.retry_policy < 0 or settings.retry_policy > 10:
            raise ValidationError(
                f"Invalid retry policy limit: {settings.retry_policy}. Must be between 0 and 10."
            )
            
        if settings.timeout <= 0.0:
            raise ValidationError(f"Invalid timeout value: {settings.timeout}. Must be greater than 0.")
            
    @staticmethod
    def validate_provider(provider: Provider) -> None:
        if provider.provider_type not in VALID_PROVIDER_TYPES:
            raise ValidationError(
                f"Invalid provider type: '{provider.provider_type}'. Must be one of {VALID_PROVIDER_TYPES}."
            )
            
        if not provider.provider_name.strip():
            raise ValidationError("Provider name cannot be empty.")
            
        if not provider.model_name.strip():
            raise ValidationError("Provider model name cannot be empty.")
