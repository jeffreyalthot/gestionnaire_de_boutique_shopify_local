from dataclasses import dataclass,field


@dataclass(frozen=True, slots=True)
class ValidationReport:
    valid: bool
    score: float
    issues: tuple[str,...]=field(default_factory=tuple)
