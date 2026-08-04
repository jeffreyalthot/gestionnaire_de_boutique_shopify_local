from __future__ import annotations

import re
from typing import Any


class AttributeNormalizer:
    def normalize(self, attributes: dict[str, Any]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, value in attributes.items():
            name = re.sub(r"[^a-z0-9]+", "_", str(key).casefold()).strip("_")[:80]
            text = " ".join(str(value).replace("\r", " ").replace("\n", " ").split())[:500]
            if name and text:
                result[name] = text
        return result
