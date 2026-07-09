from pathlib import Path

from docx import Document

from app.loaders.base import BaseDocumentLoader


class DocxLoader(BaseDocumentLoader):
    supported_extensions = (".docx",)

    def load(self, file_path: Path) -> str:
        document = Document(str(file_path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)
