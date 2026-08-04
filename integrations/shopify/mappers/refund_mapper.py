from __future__ import annotations

from decimal import Decimal

from integrations.shopify.mappers.base import gid, mapping, money, nodes, timestamp


def map_refund(node: dict[str, object]) -> dict[str, object]:
    transactions = tuple(nodes(node.get("transactions", ())))
    amount = Decimal("0")
    currencies: set[str] = set()
    mapped_transactions = []
    for transaction in transactions:
        transaction_amount, currency = money(transaction.get("amountSet", transaction.get("amount", 0)))
        amount += transaction_amount
        currencies.add(currency)
        mapped_transactions.append({
            **transaction,
            "id": gid(transaction.get("id"), "OrderTransaction"),
            "amount": transaction_amount,
            "currency": currency,
            "status": str(transaction.get("status", "") or "").lower(),
            "kind": str(transaction.get("kind", "") or "").lower(),
        })
    line_items = tuple(nodes(node.get("refundLineItems", ())))
    return {
        "id": gid(node.get("id"), "Refund"),
        "gid": str(node.get("id", "") or ""),
        "created_at": timestamp(node.get("createdAt")),
        "updated_at": timestamp(node.get("updatedAt")),
        "note": str(node.get("note", "") or ""),
        "total": amount,
        "currency": next(iter(currencies)) if len(currencies) == 1 else "MIXED" if currencies else "CAD",
        "transactions": tuple(mapped_transactions),
        "refund_line_items": line_items,
        "restock": any(bool(mapping(item).get("restockType")) for item in line_items),
        "staff_member": mapping(node.get("staffMember")),
    }
