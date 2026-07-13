import hashlib
import json
from typing import Dict, Any, Optional

class PresentationAICache:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def _hash_key(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> str:
        param_str = ""
        if params:
            param_str = json.dumps(params, sort_keys=True)
        payload = f"{prompt}:{param_str}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        key = self._hash_key(prompt, params)
        return self._store.get(key)

    def set(self, prompt: str, response: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> None:
        key = self._hash_key(prompt, params)
        self._store[key] = response
