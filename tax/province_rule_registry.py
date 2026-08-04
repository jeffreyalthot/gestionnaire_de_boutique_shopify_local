from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ProvinceTaxRule:
    province: str
    combined_rate: float
    components: tuple[tuple[str, float], ...]
    source: str = "configured"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ProvinceRuleRegistry:
    DEFAULT = {"QC": .14975, "ON": .13, "BC": .12, "AB": .05}
    COMPONENTS = {
        "QC": (("GST", .05), ("QST", .09975)),
        "ON": (("HST", .13),),
        "BC": (("GST", .05), ("PST", .07)),
        "AB": (("GST", .05),),
    }

    def __init__(self, rules: dict[str, float] | None = None) -> None:
        self.rules = {**self.DEFAULT, **{str(k).upper(): float(v) for k, v in (rules or {}).items()}}

    def rate(self, province: str) -> float:
        return self.get(province).combined_rate

    def get(self, province: str) -> ProvinceTaxRule:
        code = str(province).strip().upper()
        rate = self.rules.get(code, .05)
        return ProvinceTaxRule(code, rate, self.COMPONENTS.get(code, (("GST", rate),)), "default" if code not in self.rules else "configured")

    def register(self, province: str, rate: float, *, components: tuple[tuple[str, float], ...] = ()) -> None:
        code = str(province).strip().upper()
        if len(code) != 2 or not 0 <= rate <= 1:
            raise ValueError("règle provinciale invalide")
        self.rules[code] = float(rate)
        if components:
            self.COMPONENTS[code] = tuple((str(name), float(value)) for name, value in components)
