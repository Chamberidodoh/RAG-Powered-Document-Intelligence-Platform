from pathlib import Path

from PyPDF2 import PdfReader

from app.loaders.base import BaseDocumentLoader


class PdfLoader(BaseDocumentLoader):
    supported_extensions = (".pdf",)

    def load(self, file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(page for page in pages if page)
