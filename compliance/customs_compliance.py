from __future__ import annotations

from dataclasses import asdict,dataclass
from decimal import Decimal
import re

@dataclass(frozen=True,slots=True)
class CustomsComplianceDecision:
    valid: bool
    normalized: dict[str,object]
    errors: tuple[str,...]
    warnings: tuple[str,...]
    def as_dict(self): return asdict(self)

class CustomsCompliance:
    def evaluate(self,sku: str,hs_code: str,country_of_origin: str,unit_cost: object,*,description: str="",weight_kg: object=0) -> CustomsComplianceDecision:
        errors=[];warnings=[]; sku=str(sku).strip(); hs="".join(ch for ch in str(hs_code) if ch.isdigit()); country=str(country_of_origin).strip().upper(); cost=Decimal(str(unit_cost)); weight=Decimal(str(weight_kg))
        if not sku:errors.append("missing_sku")
        if len(hs) not in {6,8,10}:errors.append("invalid_hs_code")
        if not re.fullmatch(r"[A-Z]{2}",country):errors.append("invalid_origin_country")
        if cost<0:errors.append("invalid_unit_cost")
        if weight<0:errors.append("invalid_weight")
        if not description:warnings.append("missing_customs_description")
        normalized={"sku":sku,"harmonizedSystemCode":hs,"countryCodeOfOrigin":country,"cost":float(cost),"description":" ".join(description.split())[:255],"weightKg":float(weight)}
        return CustomsComplianceDecision(not errors,normalized,tuple(errors),tuple(warnings))

def customs_fields(sku: str,hs_code: str,country_of_origin: str,unit_cost: float) -> dict[str,object]:
    result=CustomsCompliance().evaluate(sku,hs_code,country_of_origin,unit_cost)
    if not result.valid:raise ValueError("Données douanières invalides.")
    return {k:v for k,v in result.normalized.items() if k in {"sku","harmonizedSystemCode","countryCodeOfOrigin","cost"}}
