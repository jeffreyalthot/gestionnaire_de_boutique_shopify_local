from __future__ import annotations

from pathlib import Path


class ImageCompressor:
    def compress(self, source: Path, destination: Path, *, quality: int = 85, format_name: str = "WEBP") -> dict[str, object]:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow est requis pour compresser une image.") from exc
        quality = max(40, min(95, quality))
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGB")
            image.save(destination, format=format_name, quality=quality, optimize=True, method=4)
            width, height = image.size
        return {"path": str(destination), "width": width, "height": height,
                "byte_size": destination.stat().st_size, "format": format_name.lower()}
