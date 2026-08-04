from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


class ImageHashStore:
    def __init__(self, db: Any | None = None) -> None:
        self.db = db
        self._hashes: dict[str, str] = {}

    @staticmethod
    def digest(path: Path, block_size: int = 65536) -> str:
        hasher = hashlib.sha256()
        with path.open("rb") as stream:
            while block := stream.read(block_size):
                hasher.update(block)
        return hasher.hexdigest()

    def register(self, path: Path, asset_id: str = "") -> tuple[str, bool]:
        digest = self.digest(path)
        duplicate = digest in self._hashes
        self._hashes.setdefault(digest, asset_id or str(path))
        if self.db is not None:
            duplicate = duplicate or bool(self.db.scalar("SELECT 1 FROM media_assets WHERE sha256=? LIMIT 1", (digest,), default=0))
        return digest, duplicate
