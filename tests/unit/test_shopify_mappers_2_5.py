from decimal import Decimal

from integrations.shopify.mappers.base import gid, money, nodes, pagination, timestamp
from integrations.shopify.mappers.customer_mapper import map_customer
from integrations.shopify.mappers.fulfillment_mapper import map_fulfillment
from integrations.shopify.mappers.inventory_mapper import map_inventory_level
from integrations.shopify.mappers.order_mapper import map_shopify_order
from integrations.shopify.mappers.product_mapper import map_shopify_product
from integrations.shopify.mappers.refund_mapper import map_refund
from integrations.shopify.mappers.variant_mapper import map_variant


def test_mapper_base_handles_edges_gid_money_and_page_info():
    container = {"edges": [{"node": {"id": 1}}], "pageInfo": {"hasNextPage": True, "endCursor": "c"}}
    assert nodes(container) == [{"id": 1}]
    assert pagination(container)["end_cursor"] == "c"
    assert gid("gid://shopify/Product/9", "Product") == "9"
    assert money({"shopMoney": {"amount": "10.005", "currencyCode": "cad"}}) == (Decimal("10.01"), "CAD")
    assert timestamp("2026-01-01T00:00:00Z").endswith("+00:00")


def test_product_mapper_maps_variants_options_and_pagination():
    product = map_shopify_product({
        "id": "gid://shopify/Product/1", "title": " P ", "status": "ACTIVE", "tags": ["a"],
        "variants": {"nodes": [{"id": "gid://shopify/ProductVariant/2", "price": "12", "sku": "S"}], "pageInfo": {"hasNextPage": True}},
        "options": [{"id": "gid://shopify/ProductOption/3", "name": "Color", "values": ["Red"]}],
    })
    assert product["id"] == "1" and product["variants"][0]["id"] == "2"
    assert product["options"][0]["values"] == ("Red",)
    assert product["variant_pagination"]["has_next_page"] is True


def test_variant_mapper_normalizes_commercial_fields():
    mapped = map_variant({
        "id": "gid://shopify/ProductVariant/2", "price": "12.345", "compareAtPrice": "15",
        "inventoryQuantity": 4, "selectedOptions": [{"name": "Color", "value": "Red"}],
        "inventoryItem": {"id": "gid://shopify/InventoryItem/8"},
    })
    assert mapped["price"] == Decimal("12.35")
    assert mapped["compare_at_price"] == Decimal("15.00")
    assert mapped["inventory_item_id"] == "8"


def test_order_mapper_computes_line_totals_and_statuses():
    order = map_shopify_order({
        "id": "gid://shopify/Order/1", "name": "#1", "displayFinancialStatus": "PAID",
        "currentTotalPriceSet": {"shopMoney": {"amount": "20", "currencyCode": "CAD"}},
        "lineItems": {"nodes": [{
            "id": "gid://shopify/LineItem/3", "title": "A", "currentQuantity": 2,
            "originalUnitPriceSet": {"shopMoney": {"amount": "10", "currencyCode": "CAD"}},
            "variant": {"id": "gid://shopify/ProductVariant/4", "product": {"id": "gid://shopify/Product/5"}},
        }]},
    })
    assert order["shopify_order_id"] == "1" and order["financial_status"] == "paid"
    assert order["lines"][0]["line_total"] == Decimal("20.00")
    assert order["calculated_line_total"] == Decimal("20.00")


def test_inventory_mapper_calculates_sellable_and_ids():
    mapped = map_inventory_level({
        "id": "gid://shopify/InventoryLevel/1",
        "quantities": [{"name": "available", "quantity": 8}, {"name": "reserved", "quantity": 3}],
        "location": {"id": "gid://shopify/Location/2"},
        "item": {"id": "gid://shopify/InventoryItem/3"},
    })
    assert mapped["sellable"] == 5 and mapped["location_id"] == "2" and mapped["inventory_item_id"] == "3"


def test_fulfillment_mapper_deduplicates_tracking():
    mapped = map_fulfillment({
        "id": "gid://shopify/Fulfillment/1", "status": "SUCCESS",
        "trackingInfo": [{"company": "X", "number": "1"}, {"company": "X", "number": "1"}],
    })
    assert mapped["status"] == "success" and len(mapped["tracking"]) == 1


def test_customer_mapper_can_remove_pii_and_hash_identity():
    public = map_customer({"id": "gid://shopify/Customer/1", "email": "A@B.COM", "firstName": "A"}, pii_salt="s", include_pii=False)
    assert public["id"] == "1" and public["email"] == "" and public["email_hash"]


def test_refund_mapper_totals_transactions_and_restock():
    mapped = map_refund({
        "id": "gid://shopify/Refund/1",
        "transactions": [{"id": "gid://shopify/OrderTransaction/2", "amountSet": {"shopMoney": {"amount": "3.50", "currencyCode": "CAD"}}}],
        "refundLineItems": {"nodes": [{"restockType": "RETURN"}]},
    })
    assert mapped["total"] == Decimal("3.50") and mapped["currency"] == "CAD" and mapped["restock"]
