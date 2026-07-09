from pathlib import Path

import pandas as pd

from app.loaders.base import BaseDocumentLoader


class ExcelLoader(BaseDocumentLoader):
    supported_extensions = (".xlsx",)

    def load(self, file_path: Path) -> str:
        frame = pd.read_excel(file_path)
        return frame.to_markdown(index=False)
