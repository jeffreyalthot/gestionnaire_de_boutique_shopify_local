from __future__ import annotations

import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class LocaleResolution:
    requested: str | None
    resolved: str
    fallback_used: bool
    language: str
    region: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class LocaleRegistry:
    PATTERN = re.compile(r"^[a-zA-Z]{2,3}(?:[-_][a-zA-Z]{2})?$")

    def __init__(self, locales=("fr-CA", "en-CA"), default="fr-CA") -> None:
        normalized = tuple(dict.fromkeys(self.normalize(value) for value in locales if value))
        if not normalized:
            raise ValueError("au moins une locale est requise")
        self.locales = normalized
        self.default = self.normalize(default) if self.normalize(default) in normalized else normalized[0]

    @classmethod
    def normalize(cls, locale: str) -> str:
        value = str(locale).strip().replace("_", "-")
        if not cls.PATTERN.fullmatch(value):
            return value
        parts = value.split("-")
        return parts[0].lower() + ("-" + parts[1].upper() if len(parts) > 1 else "")

    def resolve(self, requested: str | None) -> str:
        return self.resolve_details(requested).resolved

    def resolve_details(self, requested: str | None) -> LocaleResolution:
        normalized = self.normalize(requested) if requested else ""
        resolved = normalized if normalized in self.locales else next((loc for loc in self.locales if normalized and loc.split("-")[0] == normalized.split("-")[0]), self.default)
        language, _, region = resolved.partition("-")
        return LocaleResolution(requested, resolved, resolved != normalized, language, region)
