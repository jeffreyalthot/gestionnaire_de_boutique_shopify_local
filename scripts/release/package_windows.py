from __future__ import annotations
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main() -> int:
    destination=ROOT/'dist'/'windows-portable'
    if destination.exists(): shutil.rmtree(destination)
    ignored=shutil.ignore_patterns('__pycache__','.pytest_cache','*.pyc','build','dist','.venv','data/database/*.db')
    shutil.copytree(ROOT,destination,ignore=ignored)
    shutil.make_archive(str(ROOT/'dist'/'shopify-alibaba-windows-portable'),'zip',destination.parent,destination.name)
    return 0
if __name__=='__main__': raise SystemExit(main())
