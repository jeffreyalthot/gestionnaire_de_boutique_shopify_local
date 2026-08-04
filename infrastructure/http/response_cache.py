from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from infrastructure.cache.memory_cache import MemoryCache
@dataclass(frozen=True, slots=True)
class CachedResponse:
    status_code: int
    headers: dict[str, str]
    body: bytes
class ResponseCache(MemoryCache[CachedResponse]):
    @staticmethod
    def key(method: str, url: str, params: dict[str, object] | None = None) -> str:
        raw = json.dumps([method.upper(), url, params or {}], sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
