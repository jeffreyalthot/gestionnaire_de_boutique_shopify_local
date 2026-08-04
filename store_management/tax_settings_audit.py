from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class TaxSettingsAuditResult:
    valid: bool
    issues: tuple[str,...]
    warnings: tuple[str,...]
    home_country: str
    inclusive: bool|None
    registrations: int
    def as_dict(self):return asdict(self)

class TaxSettingsAudit:
    def audit(self,settings: dict[str,object]) -> dict[str,object]:return self.evaluate(settings).as_dict()
    def evaluate(self,settings: dict[str,object]) -> TaxSettingsAuditResult:
        issues=[];warnings=[];inclusive=settings.get("prices_include_tax");country=str(settings.get("home_country","")).upper();registrations=tuple(settings.get("registrations",()) or ())
        if inclusive is None:issues.append("tax_inclusion_unknown")
        if len(country)!=2:issues.append("home_country_missing")
        if not registrations:warnings.append("no_tax_registrations")
        if settings.get("taxes_included_in_shipping") is None:warnings.append("shipping_tax_unknown")
        return TaxSettingsAuditResult(not issues,tuple(issues),tuple(warnings),country,inclusive if isinstance(inclusive,bool) else None,len(registrations))
