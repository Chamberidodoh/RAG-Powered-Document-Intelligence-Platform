from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from app.loaders.base import BaseDocumentLoader


def _get_pdf_reader() -> Any:
    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue
        reader = getattr(module, "PdfReader", None)
        if reader is not None:
            return reader
    raise ImportError("No PDF reader package is available. Install pypdf or PyPDF2.")


PdfReader = _get_pdf_reader()


class PdfLoader(BaseDocumentLoader):
    supported_extensions = (".pdf",)

    def load(self, file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(page for page in pages if page)
