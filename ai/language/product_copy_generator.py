from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from ai.language.text_sanitizer import sanitize, sanitize_html
from catalog.description_generator import generate_description
from catalog.title_generator import generate_title


@dataclass(frozen=True, slots=True)
class ProductCopy:
    title: str
    description_html: str
    seo_title: str
    meta_description: str
    handle: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


class ProductCopyGenerator:
    def generate(self, title: str, attributes: dict[str, object], description: str = "") -> dict[str, str]:
        clean = generate_title(sanitize_html(title, 255))
        if not clean:
            raise ValueError("product title is required")
        normalized_attributes = {
            sanitize(str(key), 80): sanitize_html(str(value), 500)
            for key, value in attributes.items() if value not in (None, "")
        }
        description_html = generate_description(clean, normalized_attributes, sanitize(description, 5000))
        meta = sanitize_html(description_html, 320)
        if len(meta) > 160:
            meta = meta[:157].rstrip() + "..."
        seo_title = clean if len(clean) <= 70 else clean[:67].rstrip() + "..."
        handle = re.sub(r"[^a-z0-9]+", "-", clean.lower()).strip("-")[:120]
        return ProductCopy(clean, description_html, seo_title, meta, handle).as_dict()
