import json
import asyncio
import os
from typing import Any
from services.subject_intelligence.writers.base_writer import BaseWriter

class JSONWriter(BaseWriter):
    """Concrete async-safe JSON writer."""
    async def write(self, data: Any, filepath: str) -> None:
        """Write Pydantic models or dicts to path asynchronously."""
        if hasattr(data, "model_dump_json"):
            content = data.model_dump_json(indent=2)
        else:
            content = json.dumps(data, indent=2)
            
        loop = asyncio.get_event_loop()
        def write_sync():
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        await loop.run_in_executor(None, write_sync)
