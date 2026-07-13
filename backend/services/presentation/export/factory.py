from typing import Dict, Type
from services.presentation.export.interfaces.exporter import ExporterInterface

class PresentationExportFactory:
    def __init__(self) -> None:
        self._exporters: Dict[str, Type[ExporterInterface]] = {}

    def register(self, export_type: str, exporter_cls: Type[ExporterInterface]) -> None:
        self._exporters[export_type] = exporter_cls

    def get_exporter(self, export_type: str) -> ExporterInterface:
        exporter_cls = self._exporters.get(export_type)
        if not exporter_cls:
            raise ValueError(f"No exporter registered for type: {export_type}")
        return exporter_cls()

    def list_supported_types(self):
        return list(self._exporters.keys())
