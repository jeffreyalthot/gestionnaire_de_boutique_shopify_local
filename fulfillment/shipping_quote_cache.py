from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Iterable

from infrastructure.cache.memory_cache import CacheStats, MemoryCache


@dataclass(frozen=True, slots=True)
class ShippingQuoteCacheKey:
    value: str
    country: str
    postal_prefix: str
    quantity: int


class ShippingQuoteCache(MemoryCache[dict[str, object]]):
    def __init__(self, max_entries: int = 1_000, max_estimated_bytes: int = 12 * 1024 * 1024, default_ttl_seconds: int = 1_800) -> None:
        super().__init__(max_entries=max_entries, max_estimated_bytes=max_estimated_bytes)
        self.default_ttl_seconds = max(30, int(default_ttl_seconds))

    def build_key(
        self,
        product_id: str,
        sku_id: str,
        country: str,
        postal: str,
        quantity: int,
        *,
        variant_attributes: dict[str, object] | None = None,
    ) -> ShippingQuoteCacheKey:
        normalized_country = str(country).strip().upper()
        normalized_postal = "".join(str(postal).upper().split())
        postal_prefix = normalized_postal[:3]
        payload = {
            "product_id": str(product_id).strip(),
            "sku_id": str(sku_id).strip(),
            "country": normalized_country,
            "postal": normalized_postal,
            "quantity": max(1, int(quantity)),
            "variant_attributes": dict(sorted((variant_attributes or {}).items())),
        }
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()
        return ShippingQuoteCacheKey(digest, normalized_country, postal_prefix, payload["quantity"])

    def key(self, product_id: str, sku_id: str, country: str, postal: str, quantity: int) -> str:
        return self.build_key(product_id, sku_id, country, postal, quantity).value

    def store(self, key: str, quote: dict[str, object], ttl_seconds: int | None = None) -> None:
        self.set(key, dict(quote), ttl_seconds or self.default_ttl_seconds)

    def cheapest(self, keys: Iterable[str]) -> dict[str, object] | None:
        quotes = [quote for key in keys if (quote := self.get(key)) is not None]
        return min(quotes, key=lambda quote: float(quote.get("amount", quote.get("amount_cad", float("inf"))))) if quotes else None
