from __future__ import annotations

from pathlib import Path


class MediaCache:
    def __init__(self, directory: Path, max_bytes: int) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes

    def size(self) -> int:
        return sum(path.stat().st_size for path in self.directory.glob("*") if path.is_file())

    def prune(self) -> int:
        files = sorted((path for path in self.directory.glob("*") if path.is_file()), key=lambda path: path.stat().st_mtime)
        total = sum(path.stat().st_size for path in files)
        removed = 0
        while total > self.max_bytes and files:
            path = files.pop(0)
            size = path.stat().st_size
            path.unlink(missing_ok=True)
            total -= size
            removed += 1
        return removed
