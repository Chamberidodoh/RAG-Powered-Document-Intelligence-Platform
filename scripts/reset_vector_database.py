from pathlib import Path
import shutil

from app.core.config import settings

root = Path(settings.chroma_persist_directory)
if root.exists():
    shutil.rmtree(root)
root.mkdir(parents=True, exist_ok=True)
print("Reset complete")
