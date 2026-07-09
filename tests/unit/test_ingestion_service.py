from unittest.mock import Mock

import pytest

from app.core.exceptions import EmptyDocumentError, UnsupportedFileTypeError
from app.services.ingestion_service import IngestionService


class FakeUpload:
    def __init__(self, filename: str, content: str) -> None:
        self.filename = filename
        self.file = Mock()
        self.file.read.return_value = content.encode("utf-8")


def test_ingestion_service_raises_for_empty_document() -> None:
    service = IngestionService()
    with pytest.raises(EmptyDocumentError):
        service.ingest_file(FakeUpload("test.txt", "   "))
