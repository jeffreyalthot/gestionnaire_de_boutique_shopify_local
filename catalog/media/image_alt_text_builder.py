from __future__ import annotations

import re


def build_alt_text(title: str, position: int, detail: str = "") -> str:
    clean = re.sub(r"\s+", " ", f"{title} {detail}".strip())
    suffix = f" - vue {position}" if position > 1 else ""
    return (clean + suffix)[:125]
