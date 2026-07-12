import json
import os
from services.rendering.writers.base_writer import BaseWriter
from services.rendering.schemas import PresentationLayoutModel

class JsonWriter(BaseWriter):
    def write(self, model: PresentationLayoutModel, output_path: str) -> None:
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(model.model_dump(), f, indent=2)
