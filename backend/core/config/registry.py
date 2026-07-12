from typing import Dict, List
from core.config.providers import Provider
from core.config.settings import Settings
from core.config.validator import ConfigValidator
from core.config.loader import ConfigLoader
from core.config.exceptions import (
    DuplicateProviderError,
    ProviderNotFoundError
)

class ConfigRegistry:
    """Centralized configuration registry managing settings loading and AI providers."""
    
    def __init__(self, settings: Settings = None):
        self._settings = settings if settings else ConfigLoader.load()
        self._providers: Dict[str, Provider] = {}

    @property
    def settings(self) -> Settings:
        return self._settings

    def update_settings(self, settings: Settings) -> None:
        ConfigValidator.validate_settings(settings)
        self._settings = settings

    def register_provider(self, provider: Provider) -> None:
        """Registers a new AI provider, raising DuplicateProviderError if already registered."""
        if provider.provider_name in self._providers:
            raise DuplicateProviderError(f"Provider '{provider.provider_name}' is already registered.")
            
        ConfigValidator.validate_provider(provider)
        self._providers[provider.provider_name] = provider

    def get_provider(self, provider_name: str) -> Provider:
        """Retrieves a provider by name, raising ProviderNotFoundError if missing."""
        if provider_name not in self._providers:
            raise ProviderNotFoundError(f"Provider '{provider_name}' not found in registry.")
        return self._providers[provider_name]

    def list_providers(self) -> List[Provider]:
        """Lists all registered providers."""
        return list(self._providers.values())

    def validate_provider(self, provider_name: str) -> None:
        """Validates provider credentials and metadata."""
        provider = self.get_provider(provider_name)
        ConfigValidator.validate_provider(provider)
