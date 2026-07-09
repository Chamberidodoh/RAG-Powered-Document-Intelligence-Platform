from pathlib import Path

from app.loaders import get_loader_for_extension


def test_get_loader_for_supported_extensions() -> None:
    assert get_loader_for_extension(".txt").supported_extensions == (".txt", ".md")
    assert get_loader_for_extension(".pdf").supported_extensions == (".pdf",)
