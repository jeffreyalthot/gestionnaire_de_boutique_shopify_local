from __future__ import annotations
from dataclasses import asdict,dataclass
from decimal import Decimal,ROUND_HALF_UP
from tax.country_rule_registry import CountryRuleRegistry
from tax.province_rule_registry import ProvinceRuleRegistry
@dataclass(frozen=True,slots=True)
class TaxDecision:
    taxable: bool
    rate: float
    tax_cad: float
    total_cad: float
    jurisdiction: str
    issues: tuple[str,...]=()
    def to_dict(self):return asdict(self)
class TaxEngine:
    def __init__(self,countries: CountryRuleRegistry | None=None,provinces: ProvinceRuleRegistry | None=None):self.countries=countries or CountryRuleRegistry();self.provinces=provinces or ProvinceRuleRegistry()
    def calculate(self,amount_cad: float,country: str,region: str="",category: str="general") -> TaxDecision:
        amount=max(Decimal("0"),Decimal(str(amount_cad)));country=country.upper();region=region.upper();issues=[]
        if country=="CA":rate=Decimal(str(self.provinces.rate(region)));jurisdiction=f"CA-{region or 'DEFAULT'}"
        else:
            rule=self.countries.get(country);rate=Decimal(str(rule.get("rate",0) or 0));jurisdiction=country
            if not rule:issues.append("country_rule_missing")
        exempt=category in {"zero_rated","exempt"};tax=Decimal("0") if exempt else amount*rate;tax=tax.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP);total=(amount+tax).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)
        return TaxDecision(not exempt,float(rate),float(tax),float(total),jurisdiction,tuple(issues))
