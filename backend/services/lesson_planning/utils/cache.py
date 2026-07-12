import hashlib
from typing import Dict, Any, Optional

class LessonCache:
    """In-memory cache using SHA-256 hashes of input queries to prevent redundant LLM invocations."""
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def get(self, text: str) -> Optional[Dict[str, Any]]:
        h = self._hash_text(text)
        return self._cache.get(h)

    def set(self, text: str, value: Dict[str, Any]) -> None:
        h = self._hash_text(text)
        self._cache[h] = value

    def clear(self) -> None:
        self._cache.clear()
