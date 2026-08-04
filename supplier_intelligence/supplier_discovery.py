from __future__ import annotations

from dataclasses import asdict, dataclass

from supplier_intelligence.supplier_candidate import SupplierCandidate


@dataclass(frozen=True, slots=True)
class SupplierDiscoveryResult:
    accepted: tuple[SupplierCandidate, ...]
    rejected: tuple[tuple[str, tuple[str, ...]], ...]
    evaluated: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class SupplierDiscovery:
    def filter(self, candidates: list[SupplierCandidate], *, minimum_years: float = 1, require_verified: bool = True) -> tuple[SupplierCandidate, ...]:
        return self.evaluate(candidates, minimum_years=minimum_years, require_verified=require_verified).accepted

    def evaluate(self, candidates: list[SupplierCandidate], *, minimum_years: float = 1, require_verified: bool = True, minimum_response_rate: float = 0, countries: set[str] | None = None) -> SupplierDiscoveryResult:
        accepted: list[SupplierCandidate] = []; rejected: list[tuple[str, tuple[str, ...]]] = []
        for candidate in candidates:
            reasons: list[str] = []
            if candidate.years_active < minimum_years:
                reasons.append("insufficient_history")
            if require_verified and not candidate.verified:
                reasons.append("not_verified")
            response = float(getattr(candidate, "response_rate", 1) or 0)
            if response < minimum_response_rate:
                reasons.append("low_response_rate")
            country = str(getattr(candidate, "country_code", getattr(candidate, "country", ""))).upper()
            if countries and country and country not in {item.upper() for item in countries}:
                reasons.append("country_not_allowed")
            if reasons:
                rejected.append((str(getattr(candidate, "supplier_id", getattr(candidate, "id", "unknown"))), tuple(reasons)))
            else:
                accepted.append(candidate)
        return SupplierDiscoveryResult(tuple(accepted), tuple(rejected), len(candidates))
