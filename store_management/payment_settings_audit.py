from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class PaymentSettingsAuditResult:
    valid: bool
    score: float
    issues: tuple[str,...]
    warnings: tuple[str,...]
    capabilities: tuple[str,...]
    def as_dict(self):return asdict(self)

class PaymentSettingsAudit:
    def audit(self,settings: dict[str,object]) -> dict[str,object]:return self.evaluate(settings).as_dict()
    def evaluate(self,settings: dict[str,object]) -> PaymentSettingsAuditResult:
        issues=[];warnings=[];currency=str(settings.get("currency","")).upper();providers=tuple(map(str,settings.get("providers",()) or ()))
        if len(currency)!=3:issues.append("missing_currency")
        if settings.get("manual_capture") and not settings.get("capture_workflow_enabled"):issues.append("manual_capture_without_workflow")
        if not providers:warnings.append("no_payment_provider_reported")
        if settings.get("test_mode"):warnings.append("test_mode_enabled")
        if settings.get("fraud_analysis_enabled") is False:warnings.append("fraud_analysis_disabled")
        capabilities=tuple(filter(None,("manual_capture" if settings.get("manual_capture") else "automatic_capture","refunds" if settings.get("refunds_enabled",True) else "")))
        return PaymentSettingsAuditResult(not issues,round(max(0,1-len(issues)*.3-len(warnings)*.08),4),tuple(issues),tuple(warnings),capabilities)
