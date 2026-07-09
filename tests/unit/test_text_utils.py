from app.utils.text_utils import build_metadata, clean_text, split_text_into_chunks


def test_clean_text_normalizes_whitespace() -> None:
    text = "Hello\n\nworld   there"
    assert clean_text(text) == "Hello world there"


def test_split_text_into_chunks_respects_overlap() -> None:
    chunks = split_text_into_chunks("one two three four five six seven eight", chunk_size=3, chunk_overlap=1)
    assert len(chunks) == 4


def test_build_metadata_contains_document_fields() -> None:
    metadata = build_metadata("doc-1", "file.pdf", "pdf", page_number=3, chunk_index=1)
    assert metadata["document_id"] == "doc-1"
    assert metadata["filename"] == "file.pdf"
