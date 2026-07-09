from app.loaders.base import BaseDocumentLoader
from app.loaders.csv_loader import CsvLoader
from app.loaders.docx_loader import DocxLoader
from app.loaders.excel_loader import ExcelLoader
from app.loaders.pdf_loader import PdfLoader
from app.loaders.text_loader import TextLoader

LOADERS = {
    ".pdf": PdfLoader,
    ".docx": DocxLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
    ".csv": CsvLoader,
    ".xlsx": ExcelLoader,
}


def get_loader_for_extension(extension: str) -> BaseDocumentLoader:
    loader_cls = LOADERS.get(extension.lower())
    if loader_cls is None:
        raise ValueError(f"No loader available for extension {extension}")
    return loader_cls()
