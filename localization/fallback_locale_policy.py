from __future__ import annotations


class FallbackLocalePolicy:
    SUPPORTED = ("fr-CA", "en-CA", "fr", "en")

    def normalize(self, locale: str, default: str = "fr-CA") -> str:
        value = str(locale or default).replace("_", "-").strip()
        parts = value.split("-")
        normalized = parts[0].lower()
        if len(parts) > 1 and parts[1]:
            normalized += "-" + parts[1].upper()
        return normalized

    def chain(self, locale: str, default: str = "fr-CA") -> tuple[str, ...]:
        normalized = self.normalize(locale, default)
        language = normalized.split("-", 1)[0]
        normalized_default = self.normalize(default, "fr-CA")
        candidates = (normalized, language, normalized_default, normalized_default.split("-", 1)[0], "en")
        return tuple(dict.fromkeys(candidate for candidate in candidates if candidate))

    def resolve(self, locale: str, available: set[str] | tuple[str, ...], default: str = "fr-CA") -> str:
        choices = {self.normalize(item, default): item for item in available}
        for candidate in self.chain(locale, default):
            if candidate in choices:
                return choices[candidate]
        raise LookupError(f"Aucune locale disponible pour {locale}")
