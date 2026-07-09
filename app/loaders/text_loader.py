from pathlib import Path

from app.loaders.base import BaseDocumentLoader


class TextLoader(BaseDocumentLoader):
    supported_extensions = (".txt", ".md")

    def load(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")
