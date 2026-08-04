from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class ShippingSettingsAuditResult:
    valid: bool
    issues: tuple[str,...]
    warnings: tuple[str,...]
    countries_covered: tuple[str,...]
    zones: int
    rates: int
    def as_dict(self):return asdict(self)

class ShippingSettingsAudit:
    def audit(self,zones: list[dict[str,object]]) -> dict[str,object]:return self.evaluate(zones).as_dict()
    def evaluate(self,zones: list[dict[str,object]]) -> ShippingSettingsAuditResult:
        issues=[];warnings=[];countries=[];rate_count=0
        if not zones:issues.append("no_shipping_zones")
        for i,zone in enumerate(zones):
            current=tuple(str(x).upper() for x in zone.get("countries",()) if str(x));rates=tuple(zone.get("rates",()) or ())
            if not current:issues.append(f"zone_{i}_empty")
            if not rates:warnings.append(f"zone_{i}_no_rates")
            for rate in rates:
                price=float(rate.get("price",0) or 0) if isinstance(rate,dict) else 0
                if price<0:issues.append(f"zone_{i}_negative_rate")
            countries.extend(current);rate_count+=len(rates)
        duplicates=sorted({country for country in countries if countries.count(country)>1})
        if duplicates:warnings.append("country_in_multiple_zones")
        return ShippingSettingsAuditResult(not issues,tuple(issues),tuple(warnings),tuple(sorted(set(countries))),len(zones),rate_count)
