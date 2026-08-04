from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal

from infrastructure.cache.memory_cache import MemoryCache


@dataclass(frozen=True, slots=True)
class ExchangeRate:
    base: str
    quote: str
    rate: Decimal
    source: str
    observed_at: str

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["rate"] = str(self.rate)
        return data


class ExchangeRateCache(MemoryCache[ExchangeRate]):
    ttl_seconds = 3600

    @staticmethod
    def key_for(base: str, quote: str) -> str:
        return f"{str(base).upper()}:{str(quote).upper()}"

    def store_rate(self, base: str, quote: str, rate: object, *, source: str = "unknown", ttl_seconds: int | None = None) -> ExchangeRate:
        value = Decimal(str(rate))
        if value <= 0:
            raise ValueError("Taux de change invalide")
        record = ExchangeRate(str(base).upper(), str(quote).upper(), value, str(source), datetime.now(timezone.utc).isoformat())
        self.set(self.key_for(base, quote), record, ttl_seconds or self.ttl_seconds)
        return record

    def get_rate(self, base: str, quote: str) -> ExchangeRate | None:
        if str(base).upper() == str(quote).upper():
            return ExchangeRate(str(base).upper(), str(quote).upper(), Decimal("1"), "identity", datetime.now(timezone.utc).isoformat())
        return self.get(self.key_for(base, quote))

    def convert(self, amount: object, base: str, quote: str) -> Decimal:
        record = self.get_rate(base, quote)
        if record is None:
            raise KeyError(self.key_for(base, quote))
        return (Decimal(str(amount)) * record.rate).quantize(Decimal("0.01"))
