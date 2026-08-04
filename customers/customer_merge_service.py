from __future__ import annotations

from typing import Any

from customers.customer_profile import CustomerProfile


class CustomerMergeService:
    def merge(self, canonical: CustomerProfile, duplicate: CustomerProfile) -> CustomerProfile:
        if canonical.customer_id == duplicate.customer_id:
            return canonical
        preferences: dict[str, Any] = {**duplicate.preferences, **canonical.preferences}
        tags = tuple(sorted(set(canonical.tags) | set(duplicate.tags) | {f"merged:{duplicate.customer_id}"}))
        return CustomerProfile(
            customer_id=canonical.customer_id,
            email_hash=canonical.email_hash or duplicate.email_hash,
            country_code=canonical.country_code or duplicate.country_code,
            language=canonical.language or duplicate.language,
            lifetime_value_cad=max(0.0, canonical.lifetime_value_cad + duplicate.lifetime_value_cad),
            risk_score=max(canonical.risk_score, duplicate.risk_score),
            preferences=preferences,
            tags=tags,
            created_at=min(canonical.created_at, duplicate.created_at),
        )
