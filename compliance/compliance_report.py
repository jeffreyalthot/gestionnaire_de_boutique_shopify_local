from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Iterable

from compliance.base import ComplianceFinding, ComplianceResult


def compliance_summary(checks: dict[str, bool]) -> dict[str, object]:
    failed = sorted(key for key, value in checks.items() if not value)
    return {"ok": not failed, "passed": sum(checks.values()), "total": len(checks), "failed": failed}


def finding_summary(findings: Iterable[ComplianceFinding]) -> dict[str, object]:
    items = tuple(findings)
    severities = Counter(item.severity for item in items)
    return {
        "ok": not any(item.blocking for item in items),
        "total": len(items),
        "blocking": sum(item.blocking for item in items),
        "by_severity": dict(severities),
        "codes": tuple(item.code for item in items),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def report_from_result(value: ComplianceResult) -> dict[str, object]:
    return {**value.as_dict(), "summary": finding_summary(value.findings)}
