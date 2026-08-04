from __future__ import annotations

from dataclasses import asdict, dataclass

from quality.validation_report import ValidationReport


@dataclass(frozen=True, slots=True)
class CompletenessResult:
    complete: bool
    score: float
    missing: tuple[str, ...]
    invalid: tuple[str, ...]
    present: int
    total: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class CompletenessChecker:
    def check(self, data: dict[str, object], required: tuple[str, ...]) -> ValidationReport:
        result = self.assess(data, required)
        return ValidationReport(result.complete, result.score, (*result.missing, *result.invalid))

    def assess(self, data: dict[str, object], required: tuple[str, ...], *, validators: dict[str, object] | None = None) -> CompletenessResult:
        missing = tuple(name for name in required if data.get(name) in (None, "", [], {}))
        invalid: list[str] = []
        for name, validator in (validators or {}).items():
            if name in data and data.get(name) not in (None, ""):
                try:
                    valid = bool(validator(data[name])) if callable(validator) else True
                except Exception:
                    valid = False
                if not valid:
                    invalid.append(name)
        total = max(1, len(required) + len(validators or {}))
        penalties = len(missing) + len(invalid)
        score = round(max(0.0, 1 - penalties / total), 4)
        return CompletenessResult(not missing and not invalid, score, missing, tuple(invalid), total - penalties, total)
