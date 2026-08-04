from __future__ import annotations

import sys
from collections import OrderedDict
from dataclasses import dataclass
from threading import RLock
from time import monotonic
from typing import Generic, TypeVar

T = TypeVar("T")
_MISSING = object()

@dataclass(frozen=True, slots=True)
class CacheStats:
    entries: int
    hits: int
    misses: int
    evictions: int
    expirations: int
    estimated_bytes: int

@dataclass(slots=True)
class _Entry(Generic[T]):
    expires_at: float
    value: T
    estimated_bytes: int

class MemoryCache(Generic[T]):
    """Cache LRU/TTL borné, thread-safe et adapté aux machines à faible mémoire."""
    def __init__(self, max_entries: int = 512, max_estimated_bytes: int = 8 * 1024 * 1024) -> None:
        if max_entries < 1 or max_estimated_bytes < 1:
            raise ValueError("Les limites du cache doivent être positives")
        self.max_entries = max_entries
        self.max_estimated_bytes = max_estimated_bytes
        self._data: OrderedDict[str, _Entry[T]] = OrderedDict()
        self._lock = RLock()
        self._hits = self._misses = self._evictions = self._expirations = 0
        self._estimated_bytes = 0

    @staticmethod
    def _estimate(key: str, value: object) -> int:
        try:
            return max(1, sys.getsizeof(key) + sys.getsizeof(value))
        except Exception:
            return 1

    def set(self, key: str, value: T, ttl: float) -> None:
        if ttl <= 0:
            self.pop(key, None)
            return
        entry = _Entry(monotonic() + ttl, value, self._estimate(key, value))
        with self._lock:
            previous = self._data.pop(key, None)
            if previous:
                self._estimated_bytes -= previous.estimated_bytes
            self._data[key] = entry
            self._estimated_bytes += entry.estimated_bytes
            self._evict_locked()

    def _evict_locked(self) -> None:
        self._prune_locked()
        while self._data and (len(self._data) > self.max_entries or self._estimated_bytes > self.max_estimated_bytes):
            _, entry = self._data.popitem(last=False)
            self._estimated_bytes -= entry.estimated_bytes
            self._evictions += 1

    def _prune_locked(self) -> int:
        now = monotonic()
        expired = [key for key, entry in self._data.items() if entry.expires_at <= now]
        for key in expired:
            entry = self._data.pop(key)
            self._estimated_bytes -= entry.estimated_bytes
        self._expirations += len(expired)
        return len(expired)

    def get(self, key: str, default: T | None = None) -> T | None:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                self._misses += 1
                return default
            if entry.expires_at <= monotonic():
                self._data.pop(key, None)
                self._estimated_bytes -= entry.estimated_bytes
                self._expirations += 1
                self._misses += 1
                return default
            self._data.move_to_end(key)
            self._hits += 1
            return entry.value

    def pop(self, key: str, default: object = _MISSING):
        with self._lock:
            entry = self._data.pop(key, None)
            if entry is not None:
                self._estimated_bytes -= entry.estimated_bytes
                return entry.value
            if default is _MISSING:
                raise KeyError(key)
            return default

    def prune(self) -> int:
        with self._lock:
            return self._prune_locked()

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
            self._estimated_bytes = 0

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and self.get(key, _MISSING) is not _MISSING

    def __len__(self) -> int:
        with self._lock:
            self._prune_locked()
            return len(self._data)

    def stats(self) -> CacheStats:
        with self._lock:
            self._prune_locked()
            return CacheStats(len(self._data), self._hits, self._misses, self._evictions, self._expirations, self._estimated_bytes)
