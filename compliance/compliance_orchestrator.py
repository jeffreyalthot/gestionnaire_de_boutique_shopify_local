from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from compliance.base import ComplianceFinding, ComplianceResult, result


@dataclass(frozen=True, slots=True)
class RegisteredComplianceCheck:
    name: str
    check: Callable[[dict[str, Any]], ComplianceResult]
    enabled: bool = True
    critical: bool = False


class ComplianceOrchestrator:
    def __init__(self) -> None:
        self._checks: dict[str, RegisteredComplianceCheck] = {}

    def register(self, name: str, check: Callable[[dict[str, Any]], ComplianceResult], *,
                 critical: bool = False, replace: bool = False) -> None:
        if not callable(check):
            raise TypeError("check must be callable")
        if name in self._checks and not replace:
            raise ValueError(f"compliance check already registered: {name}")
        self._checks[name] = RegisteredComplianceCheck(name, check, True, critical)

    def unregister(self, name: str) -> bool:
        return self._checks.pop(name, None) is not None

    def run(self, payload: dict[str, Any]) -> ComplianceResult:
        pairs: list[tuple[str, ComplianceResult]] = []
        for item in self._checks.values():
            if not item.enabled:
                continue
            try:
                value = item.check(dict(payload))
            except Exception as exc:
                value = result(ComplianceFinding(
                    code="check_error", severity="critical" if item.critical else "high",
                    message=str(exc)[:1000], blocking=item.critical,
                    evidence={"type": type(exc).__name__}, remediation="review_check_configuration",
                ))
            pairs.append((item.name, value))
        return self.evaluate(pairs)

    def evaluate(self, checks: Iterable[tuple[str, Any]]) -> ComplianceResult:
        findings: list[ComplianceFinding] = []
        for name, check_result in checks:
            for finding in getattr(check_result, "findings", ()):
                findings.append(ComplianceFinding(
                    code=f"{name}.{finding.code}", severity=finding.severity,
                    message=finding.message, blocking=finding.blocking,
                    evidence=dict(finding.evidence), remediation=getattr(finding, "remediation", ""),
                ))
        return result(*findings)

    def snapshot(self) -> dict[str, object]:
        return {"count": len(self._checks), "checks": tuple(sorted(self._checks))}
