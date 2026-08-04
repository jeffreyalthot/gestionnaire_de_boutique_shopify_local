from __future__ import annotations

from decimal import Decimal
from typing import Any

from integrations.shopify.mappers.base import gid, mapping, money, nodes, pagination, string_tuple, timestamp


def _line_item(line: dict[str, Any], default_currency: str) -> dict[str, Any]:
    price_set = mapping(line.get("originalUnitPriceSet"))
    price, currency = money(price_set, default_currency=default_currency)
    discounted, _ = money(line.get("discountedUnitPriceSet", price_set), default_currency=currency)
    variant = mapping(line.get("variant"))
    product = mapping(variant.get("product"))
    quantity = max(0, int(line.get("currentQuantity", line.get("quantity", 0)) or 0))
    return {
        "id": gid(line.get("id"), "LineItem"),
        "gid": str(line.get("id", "") or ""),
        "title": str(line.get("title", "") or ""),
        "name": str(line.get("name", line.get("title", "")) or ""),
        "sku": str(line.get("sku", variant.get("sku", "")) or "").strip(),
        "quantity": quantity,
        "original_quantity": max(0, int(line.get("quantity", quantity) or 0)),
        "unit_price": price,
        "discounted_unit_price": discounted,
        "line_total": discounted * quantity,
        "currency": currency,
        "variant_id": gid(variant.get("id"), "ProductVariant"),
        "product_id": gid(product.get("id"), "Product"),
        "vendor": str(line.get("vendor", product.get("vendor", "")) or ""),
        "requires_shipping": bool(line.get("requiresShipping", True)),
        "taxable": bool(line.get("taxable", True)),
        "custom_attributes": tuple(nodes(line.get("customAttributes", ()))),
    }


def map_shopify_order(node: dict[str, object]) -> dict[str, object]:
    total_set = mapping(node.get("currentTotalPriceSet"))
    total, currency = money(total_set)
    subtotal, _ = money(node.get("currentSubtotalPriceSet", {}), default_currency=currency)
    tax, _ = money(node.get("currentTotalTaxSet", {}), default_currency=currency)
    shipping, _ = money(node.get("totalShippingPriceSet", {}), default_currency=currency)
    discounts, _ = money(node.get("currentTotalDiscountsSet", {}), default_currency=currency)
    line_container = mapping(node.get("lineItems"))
    customer = mapping(node.get("customer"))
    shipping_address = mapping(node.get("shippingAddress"))
    billing_address = mapping(node.get("billingAddress"))
    lines = tuple(_line_item(line, currency) for line in nodes(line_container))
    calculated_total = sum((line["line_total"] for line in lines), Decimal("0"))
    return {
        "shopify_order_id": gid(node.get("id"), "Order"),
        "gid": str(node.get("id", "") or ""),
        "legacy_id": str(node.get("legacyResourceId", "") or ""),
        "name": str(node.get("name", "") or ""),
        "email": str(node.get("email", customer.get("email", "")) or ""),
        "financial_status": str(node.get("displayFinancialStatus", "") or "").lower(),
        "fulfillment_status": str(node.get("displayFulfillmentStatus", "") or "").lower(),
        "cancelled_at": timestamp(node.get("cancelledAt")),
        "closed_at": timestamp(node.get("closedAt")),
        "created_at": timestamp(node.get("createdAt")),
        "updated_at": timestamp(node.get("updatedAt")),
        "processed_at": timestamp(node.get("processedAt")),
        "total": total,
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "discounts": discounts,
        "calculated_line_total": calculated_total,
        "currency": currency,
        "customer": customer,
        "customer_id": gid(customer.get("id"), "Customer"),
        "shipping_address": shipping_address,
        "billing_address": billing_address,
        "tags": string_tuple(node.get("tags", ())),
        "test": bool(node.get("test", False)),
        "risk_level": str(node.get("riskLevel", "") or "").lower(),
        "lines": lines,
        "line_pagination": pagination(line_container),
        "raw": dict(node),
    }
