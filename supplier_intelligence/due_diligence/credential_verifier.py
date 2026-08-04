from __future__ import annotations
from dataclasses import asdict,dataclass
from datetime import date,datetime

@dataclass(frozen=True,slots=True)
class CredentialCheck:
    name: str
    valid: bool
    reason: str
    expires_on: str=""

@dataclass(frozen=True,slots=True)
class CredentialVerification:
    valid: bool
    score: float
    checks: tuple[CredentialCheck,...]
    def as_dict(self):return asdict(self)

class CredentialVerifier:
    def verify(self,credentials: dict[str,object]) -> dict[str,object]:
        result=self.evaluate(credentials);return {"valid":result.valid,"score":result.score,"checks":{item.name:item.valid for item in result.checks},"details":[asdict(x) for x in result.checks]}
    def evaluate(self,credentials: dict[str,object]) -> CredentialVerification:
        checks=[]
        for name,value in credentials.items():
            valid=bool(value);reason="valid" if valid else "missing";expiry=""
            if isinstance(value,dict):
                valid=bool(value.get("identifier") or value.get("valid"));raw=value.get("expires_on")
                if raw:
                    expiry=raw.isoformat() if isinstance(raw,(date,datetime)) else str(raw)
                    try:
                        if date.fromisoformat(expiry[:10])<date.today():valid=False;reason="expired"
                    except ValueError:valid=False;reason="invalid_expiry"
            checks.append(CredentialCheck(str(name),valid,reason,expiry))
        score=sum(item.valid for item in checks)/max(1,len(checks));return CredentialVerification(bool(checks) and all(item.valid for item in checks),round(score,4),tuple(checks))
