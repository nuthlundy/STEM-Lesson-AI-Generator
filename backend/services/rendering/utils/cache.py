import hashlib
import json
from typing import Dict, Any, Optional

class RenderingAICache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _generate_key(self, slide_data: Dict[str, Any]) -> str:
        serialized = json.dumps(slide_data, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def get(self, slide_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        key = self._generate_key(slide_data)
        return self._cache.get(key)

    def set(self, slide_data: Dict[str, Any], enrichment: Dict[str, Any]) -> None:
        key = self._generate_key(slide_data)
        self._cache[key] = enrichment
