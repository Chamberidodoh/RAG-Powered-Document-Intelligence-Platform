from pathlib import Path

import pandas as pd

from app.loaders.base import BaseDocumentLoader


class CsvLoader(BaseDocumentLoader):
    supported_extensions = (".csv",)

    def load(self, file_path: Path) -> str:
        frame = pd.read_csv(file_path)
        return frame.to_markdown(index=False)
