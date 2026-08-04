from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path


def export_csv(rows: list[dict[str, object]], path: Path) -> Path:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({str(key) for row in rows for key in row})
    fd, temporary = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            if fields: writer.writeheader()
            for row in rows: writer.writerow({key: _safe_csv(row.get(key, "")) for key in fields})
            handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try: os.unlink(temporary)
        except OSError: pass
        raise
    return path


def _safe_csv(value: object) -> object:
    if isinstance(value, str) and value[:1] in {"=", "+", "-", "@"}: return "'" + value
    return value
