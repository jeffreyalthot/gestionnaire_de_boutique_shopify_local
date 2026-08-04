from __future__ import annotations

from compliance.privacy_compliance import pseudonymize
from integrations.shopify.mappers.base import gid, mapping, nodes, string_tuple, timestamp


def map_customer(node: dict[str, object], *, pii_salt: str = "", include_pii: bool = True) -> dict[str, object]:
    email = str(node.get("email", "") or "").strip().lower()
    phone = str(node.get("phone", "") or "").strip()
    default_address = mapping(node.get("defaultAddress"))
    return {
        "id": gid(node.get("id"), "Customer"),
        "gid": str(node.get("id", "") or ""),
        "email": email if include_pii else "",
        "phone": phone if include_pii else "",
        "email_hash": pseudonymize(email, salt=pii_salt) if email and pii_salt else "",
        "phone_hash": pseudonymize(phone, salt=pii_salt) if phone and pii_salt else "",
        "first_name": str(node.get("firstName", node.get("first_name", "")) or "") if include_pii else "",
        "last_name": str(node.get("lastName", node.get("last_name", "")) or "") if include_pii else "",
        "verified_email": bool(node.get("verifiedEmail", False)),
        "state": str(node.get("state", "") or "").lower(),
        "locale": str(node.get("locale", "") or ""),
        "tags": string_tuple(node.get("tags", ())),
        "number_of_orders": int(node.get("numberOfOrders", 0) or 0),
        "created_at": timestamp(node.get("createdAt")),
        "updated_at": timestamp(node.get("updatedAt")),
        "default_address": default_address if include_pii else {},
        "addresses": tuple(nodes(node.get("addresses", ()))) if include_pii else (),
        "tax_exempt": bool(node.get("taxExempt", False)),
        "tax_exemptions": string_tuple(node.get("taxExemptions", ())),
    }
