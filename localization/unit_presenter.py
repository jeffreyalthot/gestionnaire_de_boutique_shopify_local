from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


class UnitPresenter:
    @staticmethod
    def _number(value: object, digits: int, locale: str) -> str:
        quantizer = Decimal("1") if digits == 0 else Decimal("1." + "0" * digits)
        text = format(Decimal(str(value)).quantize(quantizer, rounding=ROUND_HALF_UP), f".{digits}f")
        return text.replace(".", ",") if str(locale).lower().startswith("fr") else text

    def weight(self, grams: float, locale: str = "fr-CA") -> str:
        value = max(0.0, float(grams))
        return f"{self._number(value / 1000, 2, locale)} kg" if value >= 1000 else f"{self._number(value, 0, locale)} g"

    def length(self, centimetres: float, locale: str = "fr-CA") -> str:
        value = max(0.0, float(centimetres))
        return f"{self._number(value, 1, locale)} cm"

    def dimensions(self, length_cm: float, width_cm: float, height_cm: float, locale: str = "fr-CA") -> str:
        return " × ".join(self._number(max(0.0, float(value)), 1, locale) for value in (length_cm, width_cm, height_cm)) + " cm"

    def money(self, amount: object, currency: str = "CAD", locale: str = "fr-CA") -> str:
        number = self._number(amount, 2, locale)
        return f"{number} $ CA" if currency.upper() == "CAD" and locale.lower().startswith("fr") else f"{currency.upper()} {number}"
