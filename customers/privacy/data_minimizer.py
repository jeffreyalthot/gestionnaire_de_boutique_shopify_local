from __future__ import annotations

from typing import Any


class DataMinimizer:
    DEFAULT_ALLOWED = {"id", "customer_id", "country_code", "language", "currency", "created_at", "updated_at", "status", "tags"}

    def minimize(self, data: dict[str, Any], *, allowed: set[str] | None = None) -> dict[str, Any]:
        keys = allowed or self.DEFAULT_ALLOWED
        return {key: value for key, value in data.items() if key in keys}
