from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CountryDecision:
    allowed: bool
    country_code: str
    reason: str

def normalize_country_code(country_code: str) -> str:
    code = country_code.strip().upper()
    if len(code) != 2 or not code.isalpha():
        raise ValueError("Le code pays doit être un code ISO alpha-2.")
    return code

def evaluate_country(country_code: str, blocked: set[str], *, allowed: set[str] | None = None) -> CountryDecision:
    code = normalize_country_code(country_code)
    blocked_codes = {normalize_country_code(item) for item in blocked}
    if code in blocked_codes:
        return CountryDecision(False, code, "Pays bloqué par la politique commerciale.")
    if allowed is not None:
        allowed_codes = {normalize_country_code(item) for item in allowed}
        if code not in allowed_codes:
            return CountryDecision(False, code, "Pays absent de la liste autorisée.")
    return CountryDecision(True, code, "Pays autorisé.")

def country_allowed(country_code: str, blocked: set[str]) -> bool:
    try:
        return evaluate_country(country_code, blocked).allowed
    except ValueError:
        return False
