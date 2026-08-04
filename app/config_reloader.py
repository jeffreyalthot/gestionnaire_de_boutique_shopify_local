from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Any


@dataclass(frozen=True, slots=True)
class ConfigRevision:
    revision: str
    files: tuple[str, ...]
    values: dict[str, Any]


class ConfigReloader:
    """Charge JSON et YAML; garde la dernière révision entièrement valide."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self._lock = RLock()
        self._revision = ConfigRevision("", (), {})

    def _safe_path(self, relative: str | Path) -> Path:
        path = (self.root / relative).resolve()
        if self.root not in path.parents and path != self.root:
            raise ValueError("Chemin de configuration hors racine.")
        return path

    @staticmethod
    def _parse(path: Path) -> Any:
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".json":
            return json.loads(text)
        try:
            import yaml  # type: ignore
        except ImportError:
            result: dict[str, Any] = {}
            for raw in text.splitlines():
                line = raw.split("#", 1)[0].strip()
                if not line or ":" not in line or line.startswith("-"):
                    continue
                key, value = line.split(":", 1)
                value = value.strip()
                if value.lower() in {"true", "false"}:
                    parsed: Any = value.lower() == "true"
                else:
                    try:
                        parsed = int(value)
                    except ValueError:
                        try:
                            parsed = float(value)
                        except ValueError:
                            parsed = value.strip("'\"")
                result[key.strip()] = parsed
            return result
        return yaml.safe_load(text) or {}

    def load(self, files: tuple[str, ...]) -> ConfigRevision:
        with self._lock:
            values: dict[str, Any] = {}
            material: list[bytes] = []
            normalized: list[str] = []
            for relative in files:
                path = self._safe_path(relative)
                if not path.is_file():
                    raise FileNotFoundError(path)
                parsed = self._parse(path)
                values[relative] = parsed
                material.append(path.read_bytes())
                normalized.append(relative)
            revision = hashlib.sha256(b"\x00".join(material)).hexdigest()
            self._revision = ConfigRevision(revision, tuple(normalized), values)
            return self._revision

    def current(self) -> ConfigRevision:
        with self._lock:
            return self._revision
