from abc import ABC, abstractmethod
from typing import List, Union, Protocol
import fitz  # PyMuPDF
from services.document_intelligence.interfaces import DocumentBlock, ExtractedAsset

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, page: fitz.Page, page_number: int) -> List[Union[DocumentBlock, ExtractedAsset]]:
        """
        Extract content from a given PyMuPDF Page.
        
        Args:
            page: fitz.Page instance to extract from.
            page_number: 1-indexed page number of the page.
            
        Returns:
            A list containing DocumentBlock and/or ExtractedAsset objects.
        """
        pass
class BaseAssetSaver(Protocol):
    """Protocol representing a pluggable asset saving engine."""
    def save_asset(self, page_number: int, asset_type: str, index: int, extension: str, data: bytes) -> str:
        """
        Saves the asset and returns the relative path inside the workspace.
        """
        ...
