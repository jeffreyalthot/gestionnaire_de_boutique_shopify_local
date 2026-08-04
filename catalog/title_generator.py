from __future__ import annotations

import re
import unicodedata


def generate_title(raw_title: str, maximum: int = 120) -> str:
    clean = unicodedata.normalize("NFKC", str(raw_title))
    clean = re.sub(r"[\x00-\x1f]", "", clean)
    clean = re.sub(r"\s+", " ", clean).strip(" ,;:-")
    clean = re.sub(r"(?i)\b(?:best|hot sale|free shipping|202[0-9])\b", "", clean)
    clean = re.sub(r"\s+", " ", clean).strip(" ,;:-")
    if maximum <= 0:
        return ""
    return clean[:maximum].rstrip(" ,;:-")
