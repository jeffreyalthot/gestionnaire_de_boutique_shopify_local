from __future__ import annotations

from typing import Any


class CustomerPreferences:
    ALLOWED = {"language", "currency", "marketing_email", "marketing_sms", "preferred_channel", "timezone"}

    def normalize(self, values: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values.items():
            normalized = key.strip().lower()
            if normalized not in self.ALLOWED:
                continue
            if normalized.startswith("marketing_"):
                result[normalized] = bool(value)
            else:
                result[normalized] = str(value).strip()[:100]
        return result
