from __future__ import annotations

import html
import re


def seo_fields(title: str, description: str, *, brand: str = "", product_type: str = "") -> dict[str, str]:
    text = re.sub("<[^>]+>", " ", str(description))
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    clean_title = re.sub(r"\s+", " ", str(title)).strip()
    seo_title = clean_title
    suffix = " · ".join(value for value in (brand.strip(), product_type.strip()) if value)
    if suffix and suffix.lower() not in seo_title.lower():
        seo_title = f"{seo_title} · {suffix}"
    seo_title = seo_title[:70].rstrip(" ,;:-")
    meta = text[:160].rstrip()
    if len(text) > 160:
        meta = meta[:157].rstrip() + "..."
    handle = re.sub(r"[^a-z0-9]+", "-", clean_title.lower()).strip("-")[:120]
    return {"title": seo_title, "description": meta, "handle": handle}
