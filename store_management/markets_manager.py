from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class MarketAudit:
    market: str
    valid: bool
    countries: tuple[str,...]
    currency: str
    languages: tuple[str,...]
    issues: tuple[str,...]
    warnings: tuple[str,...]
    def as_dict(self):return asdict(self)

class MarketsManager:
    def validate(self,markets: list[dict[str,object]]) -> tuple[str,...]:return tuple(item.market for item in self.audit(markets) if not item.valid)
    def audit(self,markets: list[dict[str,object]]) -> tuple[MarketAudit,...]:
        result=[];seen_countries={}
        for index,item in enumerate(markets):
            name=str(item.get("name") or f"market-{index}");countries=tuple(sorted({str(x).upper() for x in item.get("countries",()) if str(x)}));currency=str(item.get("currency","")).upper();languages=tuple(sorted({str(x) for x in item.get("languages",item.get("locales",())) if str(x)}));issues=[];warnings=[]
            if not countries:issues.append("missing_countries")
            if len(currency)!=3:issues.append("invalid_currency")
            if not languages:warnings.append("missing_languages")
            overlaps=tuple(country for country in countries if country in seen_countries)
            if overlaps:warnings.append("overlapping_countries")
            for country in countries:seen_countries[country]=name
            result.append(MarketAudit(name,not issues,countries,currency,languages,tuple(issues),tuple(warnings)))
        return tuple(result)
    def routing_table(self,markets: list[dict[str,object]]) -> dict[str,str]:
        return {country:audit.market for audit in self.audit(markets) for country in audit.countries if audit.valid}
