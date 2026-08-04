from __future__ import annotations

from app.version import VERSION

from dashboard.pages.common import money


def render_finance(state: dict[str, object], width: int = 94) -> list[str]:
    f=state["finance"]
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 5/8 FINANCE",
        "="*width,
        f"Revenue={money(f.get('revenue'))} Supplier={money(f.get('supplier_cost'))}",
        f"Shipping={money(f.get('shipping'))} Fees={money(f.get('fees'))} Profit={money(f.get('profit'))}",
        "-"*width,
        "LEDGER: immutable double-entry postings grouped by transaction ID.",
        "RESERVES: refund, chargeback, duty, tax, marketing and supplier-payment exposure.",
        "PROFIT: order/product/supplier/channel views with currency and shipping variance.",
        "RECONCILIATION: Shopify payouts, supplier payments, refunds, fees, ledger and bank references.",
        "FINANCIAL ACTIONS: explicit approval, CAD ceiling, idempotency key and audit-chain entry.",
        "-"*width,
        "CLOSE: daily snapshot, monthly period lock, anomaly scan and backup checkpoint.",
    ]
