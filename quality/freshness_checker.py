from datetime import datetime,timezone
from quality.validation_report import ValidationReport


class FreshnessChecker:
    def check(self,updated_at: datetime,max_age_seconds: int) -> ValidationReport:
        age=(datetime.now(timezone.utc)-updated_at).total_seconds(); valid=age<=max_age_seconds; return ValidationReport(valid,1 if valid else 0,("stale",) if not valid else ())
