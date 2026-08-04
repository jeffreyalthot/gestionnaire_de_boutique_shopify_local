from __future__ import annotations

import re
from hashlib import sha1


def generate_sku(product_id: str, options: dict[str, object], prefix: str = "ALI") -> str:
    option_text = "-".join(str(value) for _, value in sorted(options.items()))
    clean = re.sub(r"[^A-Z0-9]+", "-", f"{prefix}-{product_id}-{option_text}".upper()).strip("-")
    digest = sha1(f"{product_id}|{option_text}".encode()).hexdigest()[:6].upper()
    return f"{clean[:40]}-{digest}"
