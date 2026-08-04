from __future__ import annotations

import hashlib
import json
from typing import Any


def _canonical(value: Any) -> str:
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, (dict, list, tuple, set)):
        serializable = sorted(value, key=repr) if isinstance(value, set) else value
        return json.dumps(serializable, sort_keys=True, separators=(",", ":"), default=str, ensure_ascii=True)
    return str(value)


def cache_key(namespace: str, *parts: object, max_length: int = 240) -> str:
    """Construit une clé stable, sûre et de longueur bornée."""
    namespace = str(namespace).strip().lower().replace(" ", "_")
    if not namespace or any(ch in namespace for ch in "\r\n\0:"):
        raise ValueError("cache_namespace_invalid")
    body = ":".join(_canonical(part) for part in parts)
    candidate = namespace + (":" + body if body else "")
    if len(candidate) <= max_length:
        return candidate
    digest = hashlib.sha256(candidate.encode("utf-8")).hexdigest()
    prefix_size = max(1, max_length - len(digest) - 1)
    return candidate[:prefix_size] + ":" + digest


def namespaced(namespace: str):
    return lambda *parts: cache_key(namespace, *parts)
