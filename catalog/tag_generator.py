from __future__ import annotations

import re
import unicodedata
from typing import Iterable


def generate_tags(title: str, category: str, supplier: str = "", extra: Iterable[str] = ()) -> list[str]:
    normalized = unicodedata.normalize("NFKD", str(title)).encode("ascii", "ignore").decode("ascii")
    words = [word.lower() for word in re.findall(r"[A-Za-z0-9]{4,}", normalized)]
    values = ["alibaba-import", category.strip().lower(), supplier.strip().lower(), *extra, *words[:12]]
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        tag = re.sub(r"\s+", "-", str(value).strip().lower())[:255]
        if tag and tag not in seen:
            seen.add(tag); result.append(tag)
        if len(result) >= 20:
            break
    return result
