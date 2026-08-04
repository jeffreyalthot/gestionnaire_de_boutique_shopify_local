from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Iterable, Mapping


MONEY_QUANTUM = Decimal("0.01")


def mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def nodes(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, Mapping):
        collection = value.get("nodes", value.get("edges", ()))
    else:
        collection = value
    result: list[dict[str, Any]] = []
    for item in collection or ():
        if isinstance(item, Mapping) and "node" in item and isinstance(item.get("node"), Mapping):
            result.append(dict(item["node"]))
        elif isinstance(item, Mapping):
            result.append(dict(item))
    return result


def gid(value: Any, resource: str = "") -> str:
    text = str(value or "").strip()
    if text.startswith("gid://shopify/"):
        parts = text.split("/")
        if resource and len(parts) >= 2 and parts[-2].lower() != resource.lower():
            return text
        return parts[-1]
    return text


def decimal_value(value: Any, default: Decimal = Decimal("0")) -> Decimal:
    try:
        number = Decimal(str(value if value not in (None, "") else default))
    except (InvalidOperation, ValueError, TypeError):
        return default
    return number if number.is_finite() else default


def money(value: Any, *, default_currency: str = "CAD") -> tuple[Decimal, str]:
    source = mapping(value)
    if "shopMoney" in source:
        source = mapping(source["shopMoney"])
    elif "presentmentMoney" in source and "amount" not in source:
        source = mapping(source["presentmentMoney"])
    amount = decimal_value(source.get("amount", value if not source else 0)).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)
    currency = str(source.get("currencyCode", default_currency) or default_currency).upper()
    return amount, currency


def timestamp(value: Any) -> str:
    if value in (None, ""):
        return ""
    text = str(value).strip()
    try:
        moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return text
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).isoformat()


def string_tuple(value: Any) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    if isinstance(value, str):
        return tuple(part.strip() for part in value.split(",") if part.strip())
    if isinstance(value, Iterable):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return (str(value),)


def pagination(value: Any) -> dict[str, Any]:
    source = mapping(value)
    page_info = mapping(source.get("pageInfo"))
    return {
        "has_next_page": bool(page_info.get("hasNextPage", False)),
        "has_previous_page": bool(page_info.get("hasPreviousPage", False)),
        "start_cursor": str(page_info.get("startCursor", "") or ""),
        "end_cursor": str(page_info.get("endCursor", "") or ""),
    }
