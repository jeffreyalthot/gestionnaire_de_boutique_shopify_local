from __future__ import annotations
from typing import Generic, TypeVar
from infrastructure.cache.memory_cache import MemoryCache
T = TypeVar("T")
class TTLCache(MemoryCache[T], Generic[T]):
    def __init__(self, default_ttl: float = 300.0, **kwargs: object) -> None:
        super().__init__(**kwargs)
        if default_ttl <= 0:
            raise ValueError("default_ttl doit être positif")
        self.default_ttl = float(default_ttl)
    def put(self, key: str, value: T, ttl: float | None = None) -> None:
        self.set(key, value, self.default_ttl if ttl is None else ttl)
