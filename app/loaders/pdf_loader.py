from pathlib import Path

try:
    from PyPDF2 import PdfReader
except ImportError:  # pragma: no cover - compatibility for pypdf
    from pypdf import PdfReader

from app.loaders.base import BaseDocumentLoader


class PdfLoader(BaseDocumentLoader):
    supported_extensions = (".pdf",)

    def load(self, file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(page for page in pages if page)
