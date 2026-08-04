from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class ComplianceFinding:
    code: str
    severity: str
    message: str
    blocking: bool = False
    evidence: dict[str, Any] = field(default_factory=dict)
    remediation: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ComplianceResult:
    passed: bool
    findings: tuple[ComplianceFinding, ...]
    review_required: bool
    score: float = 1.0
    evaluated_at: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "review_required": self.review_required,
            "score": self.score,
            "evaluated_at": self.evaluated_at,
            "findings": tuple(item.as_dict() for item in self.findings),
        }


def result(*findings: ComplianceFinding) -> ComplianceResult:
    severity_penalty = {"info": .01, "low": .03, "medium": .08, "high": .20, "critical": .40}
    score = max(0.0, 1.0 - sum(severity_penalty.get(item.severity.lower(), .05) for item in findings))
    return ComplianceResult(
        not any(item.blocking for item in findings),
        tuple(findings),
        bool(findings),
        round(score, 4),
        datetime.now(timezone.utc).isoformat(),
    )


def merge_results(results: Iterable[ComplianceResult]) -> ComplianceResult:
    findings = tuple(finding for item in results for finding in item.findings)
    return result(*findings)
