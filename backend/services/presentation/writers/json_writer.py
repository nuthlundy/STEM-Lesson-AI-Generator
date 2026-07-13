import json
import os
from services.presentation.writers.base_writer import BasePresentationWriter
from services.presentation.schemas import PresentationSessionModel

class JsonPresentationWriter(BasePresentationWriter):
    def write(self, model: PresentationSessionModel, output_path: str) -> None:
        dir_name = os.path.dirname(output_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(model.model_dump(), f, indent=2)
