from abc import ABC, abstractmethod
from pathlib import Path


class BaseDocumentLoader(ABC):
    supported_extensions: tuple[str, ...] = ()

    @abstractmethod
    def load(self, file_path: Path) -> str:
        """Extract text from a file."""
