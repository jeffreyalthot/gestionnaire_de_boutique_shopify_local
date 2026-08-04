from __future__ import annotations

from pathlib import Path


class ImageResizer:
    def resize(self, source: Path, destination: Path, *, maximum: int = 2048) -> dict[str, object]:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow est requis pour redimensionner une image.") from exc
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            image.thumbnail((maximum, maximum))
            image.save(destination, optimize=True)
            width, height = image.size
        return {"path": str(destination), "width": width, "height": height, "byte_size": destination.stat().st_size}
