from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True, slots=True)
class CustomsLine:
    description: str
    quantity: int
    value: Decimal
    harmonized_system_code: str
    country_code_of_origin: str
    weight_kg: Decimal = Decimal("0")

    @property
    def total_value(self) -> Decimal:
        return (self.value * self.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def as_shopify(self) -> dict[str, object]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "value": float(self.value),
            "harmonizedSystemCode": self.harmonized_system_code,
            "countryCodeOfOrigin": self.country_code_of_origin,
            "weight": float(self.weight_kg),
        }

    def as_dict(self) -> dict[str, object]:
        data = asdict(self)
        data.update(value=str(self.value), weight_kg=str(self.weight_kg), total_value=str(self.total_value))
        return data


class CustomsDataBuilder:
    def build_line(self, description: str, quantity: int, value: object, hs_code: str, origin: str, *, weight_kg: object = 0) -> CustomsLine:
        description = " ".join(str(description).split())[:255]
        quantity = int(quantity)
        amount = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        weight = Decimal(str(weight_kg)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
        hs = "".join(ch for ch in str(hs_code) if ch.isdigit())
        country = str(origin).strip().upper()
        if not description:
            raise ValueError("description douanière requise")
        if quantity <= 0 or amount < 0 or weight < 0:
            raise ValueError("quantité, valeur ou poids invalide")
        if hs and len(hs) not in {6, 8, 10}:
            raise ValueError("code SH invalide")
        if len(country) != 2 or not country.isalpha():
            raise ValueError("pays d'origine invalide")
        return CustomsLine(description, quantity, amount, hs, country, weight)

    def manifest(self, lines: list[dict[str, object]]) -> dict[str, object]:
        built = [self.build_line(**line) for line in lines]
        return {
            "lines": [line.as_shopify() for line in built],
            "total_value": str(sum((line.total_value for line in built), Decimal("0"))),
            "total_weight_kg": str(sum((line.weight_kg * line.quantity for line in built), Decimal("0"))),
        }


def build_customs_line(description: str, quantity: int, value: float, hs_code: str, origin: str) -> dict[str, object]:
    return CustomsDataBuilder().build_line(description, quantity, value, hs_code, origin).as_shopify()
