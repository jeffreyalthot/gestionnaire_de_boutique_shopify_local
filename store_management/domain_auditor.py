from __future__ import annotations
import ipaddress
from dataclasses import asdict,dataclass
from urllib.parse import urlparse

@dataclass(frozen=True,slots=True)
class DomainAuditResult:
    valid: bool
    normalized_domain: str
    canonical_domain: str
    issues: tuple[str,...]
    warnings: tuple[str,...]
    def as_dict(self):return asdict(self)

class DomainAuditor:
    def audit(self,domain: str,canonical: str) -> dict[str,object]:return self.evaluate(domain,canonical).as_dict()
    def evaluate(self,domain: str,canonical: str) -> DomainAuditResult:
        parsed=urlparse(domain if "://" in domain else "https://"+domain);canonical_host=urlparse(canonical if "://" in canonical else "https://"+canonical).hostname or "";host=parsed.hostname or "";issues=[];warnings=[]
        if parsed.scheme!="https":issues.append("https_required")
        if host.casefold()!=canonical_host.casefold():issues.append("canonical_mismatch")
        if parsed.username or parsed.password:issues.append("credentials_in_url")
        try:
            if host and (ipaddress.ip_address(host).is_private or ipaddress.ip_address(host).is_loopback):issues.append("private_address")
        except ValueError:pass
        if host.startswith("www.") and not canonical_host.startswith("www."):warnings.append("www_redirect_required")
        return DomainAuditResult(not issues,f"https://{host}" if host else "",canonical_host,tuple(issues),tuple(warnings))
