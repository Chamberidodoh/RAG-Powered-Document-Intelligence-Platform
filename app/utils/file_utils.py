from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.core.exceptions import UnsupportedFileTypeError
from app.core.security import ALLOWED_EXTENSIONS, sanitize_filename


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def validate_file(filename: str, content_type: str | None = None) -> None:
    extension = get_file_extension(filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise UnsupportedFileTypeError(f"Unsupported file type: {extension}")

    if content_type and content_type not in {"application/octet-stream"}:
        pass


def save_uploaded_file(uploaded_file: Any, destination_dir: Path | None = None) -> Path:
    destination_dir = destination_dir or settings.upload_path
    destination_dir.mkdir(parents=True, exist_ok=True)
    safe_name = sanitize_filename(uploaded_file.filename or "document")
    destination = destination_dir / safe_name
    with destination.open("wb") as handle:
        handle.write(uploaded_file.file.read())
    return destination


def get_file_size_bytes(file_path: Path) -> int:
    return file_path.stat().st_size


def get_relative_path(path: Path) -> str:
    return os.path.relpath(path, start=Path.cwd())
