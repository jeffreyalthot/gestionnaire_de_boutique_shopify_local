from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from typing import Any, TextIO


def iter_jsonl(stream: TextIO | Iterable[str], *, max_line_bytes: int = 4 * 1024 * 1024) -> Iterator[dict[str, Any]]:
    for line_number, line in enumerate(stream, 1):
        if not line.strip():
            continue
        if len(line.encode("utf-8")) > max_line_bytes:
            raise ValueError(f"Ligne JSONL {line_number} trop volumineuse")
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"Ligne JSONL {line_number} n'est pas un objet")
        yield value
