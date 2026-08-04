from __future__ import annotations

from pathlib import Path


class ImageMetadataScrubber:
    def scrub(self, source: Path, destination: Path) -> dict[str, object]:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow est requis pour retirer les métadonnées d'image.") from exc
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            clean = Image.new(image.mode, image.size)
            clean.putdata(list(image.getdata()))
            clean.save(destination, format=image.format, optimize=True)
        return {"path": str(destination), "byte_size": destination.stat().st_size, "metadata_removed": True}
