from __future__ import annotations

import re
from dataclasses import asdict, dataclass


_POSTAL_PATTERNS = {
    "CA": re.compile(r"^[A-Z]\d[A-Z][ -]?\d[A-Z]\d$", re.I),
    "US": re.compile(r"^\d{5}(?:-\d{4})?$"),
    "GB": re.compile(r"^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$", re.I),
}


@dataclass(frozen=True, slots=True)
class AddressValidationResult:
    valid: bool
    normalized: dict[str, object]
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AddressValidator:
    REQUIRED = ("firstName", "lastName", "address1", "city", "countryCodeV2", "zip")

    def validate(self, address: dict[str, object]) -> AddressValidationResult:
        normalized = {str(k): self._clean(v) for k, v in dict(address or {}).items()}
        if "countryCode" in normalized and "countryCodeV2" not in normalized:
            normalized["countryCodeV2"] = normalized["countryCode"]
        country = str(normalized.get("countryCodeV2", "")).upper()
        normalized["countryCodeV2"] = country
        postal = str(normalized.get("zip", "")).upper()
        normalized["zip"] = postal
        errors = [f"Champ manquant: {name}" for name in self.REQUIRED if not str(normalized.get(name, "")).strip()]
        warnings: list[str] = []
        pattern = _POSTAL_PATTERNS.get(country)
        if postal and pattern and not pattern.fullmatch(postal):
            errors.append("Code postal invalide pour le pays")
        if len(str(normalized.get("address1", ""))) > 120:
            errors.append("Adresse trop longue")
        if str(normalized.get("phone", "")) and len(re.sub(r"\D", "", str(normalized["phone"]))) < 7:
            warnings.append("Téléphone possiblement invalide")
        if not str(normalized.get("provinceCode", "")) and country in {"CA", "US"}:
            warnings.append("Province ou État manquant")
        return AddressValidationResult(not errors, normalized, tuple(errors), tuple(warnings))

    @staticmethod
    def _clean(value: object) -> object:
        if not isinstance(value, str):
            return value
        return " ".join(value.replace("\x00", "").split()).strip()


def validate_shipping_address(address: dict[str, object]) -> list[str]:
    """API historique: retourne seulement la liste des erreurs."""
    return list(AddressValidator().validate(address).errors)
