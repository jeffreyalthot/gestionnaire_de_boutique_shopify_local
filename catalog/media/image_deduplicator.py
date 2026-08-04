from __future__ import annotations

from pathlib import Path


class ImageDeduplicator:
    def unique(self, paths: list[Path]) -> list[Path]:
        seen: set[str] = set()
        output: list[Path] = []
        for path in paths:
            key = path.stem.lower()
            if key not in seen:
                seen.add(key)
                output.append(path)
        return output
