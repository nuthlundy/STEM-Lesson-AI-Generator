import json
import os
import datetime
from typing import Dict, Any, List, Callable
from core.diagnostics.exceptions import DuplicateProviderError, BrokenProviderError

class DiagnosticsManager:
    def __init__(self):
        self._providers: Dict[str, Callable[[], Dict[str, Any]]] = {}

    def register_provider(self, name: str, provider_fn: Callable[[], Dict[str, Any]]) -> None:
        if name in self._providers:
            raise DuplicateProviderError(f"Diagnostic provider '{name}' is already registered.")
        self._providers[name] = provider_fn

    def unregister_provider(self, name: str) -> None:
        if name in self._providers:
            del self._providers[name]

    def list_providers(self) -> List[str]:
        return list(self._providers.keys())

    def run_all(self) -> Dict[str, Any]:
        results = {}
        for name, provider_fn in self._providers.items():
            try:
                res = provider_fn()
                results[name] = res
            except Exception as e:
                raise BrokenProviderError(f"Diagnostic provider '{name}' failed: {e}")
        return results

_global_manager = DiagnosticsManager()

def get_diagnostics_manager() -> DiagnosticsManager:
    return _global_manager
