from app.loaders import get_loader_for_extension
from app.loaders.pdf_loader import PdfLoader


def test_get_loader_for_supported_extensions() -> None:
    assert get_loader_for_extension(".txt").supported_extensions == (".txt", ".md")
    assert get_loader_for_extension(".pdf").supported_extensions == (".pdf",)


def test_pdf_loader_can_be_imported() -> None:
    assert PdfLoader().supported_extensions == (".pdf",)
