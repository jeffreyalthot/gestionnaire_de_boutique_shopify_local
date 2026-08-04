from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import date,datetime,timedelta

@dataclass(frozen=True,slots=True)
class CertificationResult:
    valid: bool
    status: str
    issuer: str
    identifier: str
    expires_on: str
    days_remaining: int|None
    warnings: tuple[str,...]
    def as_dict(self):return asdict(self)

class CertificationVerifier:
    def verify(self,cert: dict[str,object]) -> tuple[bool,str]:
        result=self.evaluate(cert);return result.valid,result.status
    def evaluate(self,cert: dict[str,object],*,trusted_issuers: set[str]|None=None,warning_days: int=90) -> CertificationResult:
        issuer=str(cert.get("issuer","")).strip();identifier=str(cert.get("identifier","")).strip();raw=cert.get("expires_on");warnings=[]
        if not issuer or not identifier:return CertificationResult(False,"incomplete",issuer,identifier,"",None,())
        expiry=None
        if isinstance(raw,datetime):expiry=raw.date()
        elif isinstance(raw,date):expiry=raw
        elif raw:
            try:expiry=date.fromisoformat(str(raw)[:10])
            except ValueError:return CertificationResult(False,"invalid_expiry",issuer,identifier,str(raw),None,())
        days=(expiry-date.today()).days if expiry else None
        if expiry and days<0:return CertificationResult(False,"expired",issuer,identifier,expiry.isoformat(),days,())
        if days is not None and days<=warning_days:warnings.append("expires_soon")
        if trusted_issuers is not None and issuer not in trusted_issuers:warnings.append("untrusted_issuer")
        return CertificationResult("untrusted_issuer" not in warnings,"valid" if not warnings else "review",issuer,identifier,expiry.isoformat() if expiry else "",days,tuple(warnings))
