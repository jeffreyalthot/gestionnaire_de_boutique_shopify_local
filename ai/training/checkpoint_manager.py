from __future__ import annotations

import gzip
import hashlib
import json
import os
import pickle
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


@dataclass(frozen=True, slots=True)
class CheckpointMetadata:
    path: str
    sha256: str
    byte_size: int
    created_at: str
    serializer: str
    model_type: str
    metrics: dict[str, float]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CheckpointManager:
    """Atomic model checkpointing with integrity metadata and retention."""

    def __init__(self, *, keep_last: int = 5) -> None:
        self.keep_last = max(1, int(keep_last))

    def save(
        self,
        model: object,
        path: Path,
        *,
        metrics: dict[str, float] | None = None,
    ) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = pickle.dumps(model, protocol=pickle.HIGHEST_PROTOCOL)
        compressed = gzip.compress(payload, compresslevel=3)
        with NamedTemporaryFile("wb", delete=False, dir=path.parent, prefix=f".{path.name}.") as handle:
            handle.write(compressed)
            handle.flush()
            os.fsync(handle.fileno())
            temporary = Path(handle.name)
        os.replace(temporary, path)
        digest = hashlib.sha256(compressed).hexdigest()
        metadata = CheckpointMetadata(
            path=path.name,
            sha256=digest,
            byte_size=len(compressed),
            created_at=datetime.now(timezone.utc).isoformat(),
            serializer="pickle+gzip",
            model_type=f"{type(model).__module__}.{type(model).__qualname__}",
            metrics={str(key): float(value) for key, value in (metrics or {}).items()},
        )
        self._metadata_path(path).write_text(
            json.dumps(metadata.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        self._prune(path.parent, path.suffix)
        return path

    def load(self, path: Path, *, verify: bool = True) -> Any:
        path = Path(path)
        data = path.read_bytes()
        if verify:
            metadata = self.metadata(path)
            if metadata and hashlib.sha256(data).hexdigest() != metadata.sha256:
                raise ValueError(f"checkpoint integrity check failed: {path}")
        return pickle.loads(gzip.decompress(data))

    def metadata(self, path: Path) -> CheckpointMetadata | None:
        metadata_path = self._metadata_path(Path(path))
        if not metadata_path.is_file():
            return None
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
        return CheckpointMetadata(
            path=str(payload.get("path", "")),
            sha256=str(payload.get("sha256", "")),
            byte_size=int(payload.get("byte_size", 0)),
            created_at=str(payload.get("created_at", "")),
            serializer=str(payload.get("serializer", "")),
            model_type=str(payload.get("model_type", "")),
            metrics={str(k): float(v) for k, v in dict(payload.get("metrics", {})).items()},
        )

    def promote(self, checkpoint: Path, active_path: Path) -> Path:
        checkpoint = Path(checkpoint)
        active_path = Path(active_path)
        self.load(checkpoint, verify=True)
        active_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = active_path.with_suffix(active_path.suffix + ".tmp")
        shutil.copy2(checkpoint, temporary)
        os.replace(temporary, active_path)
        metadata_source = self._metadata_path(checkpoint)
        if metadata_source.is_file():
            shutil.copy2(metadata_source, self._metadata_path(active_path))
        return active_path

    def list(self, directory: Path, suffix: str = ".joblib") -> tuple[Path, ...]:
        def sort_key(item: Path) -> tuple[str, int, str]:
            metadata = self.metadata(item)
            created_at = metadata.created_at if metadata else ""
            try:
                modified_ns = item.stat().st_mtime_ns
            except OSError:
                modified_ns = 0
            return created_at, modified_ns, item.name

        return tuple(
            sorted(Path(directory).glob(f"*{suffix}"), key=sort_key, reverse=True)
        )

    def _prune(self, directory: Path, suffix: str) -> None:
        for old in self.list(directory, suffix)[self.keep_last:]:
            old.unlink(missing_ok=True)
            self._metadata_path(old).unlink(missing_ok=True)

    @staticmethod
    def _metadata_path(path: Path) -> Path:
        return path.with_suffix(path.suffix + ".json")
