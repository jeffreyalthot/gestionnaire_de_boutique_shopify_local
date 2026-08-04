from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ManifestAsset:
    source_url: str
    sha256: str
    content_type: str
    byte_size: int
    local_path: str
    rights_status: str
    alt_text: str


@dataclass(slots=True)
class MediaManifest:
    product_id: str
    assets: list[ManifestAsset] = field(default_factory=list)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps({"product_id": self.product_id, "assets": [asdict(item) for item in self.assets]}, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(path)
