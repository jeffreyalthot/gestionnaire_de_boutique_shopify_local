from __future__ import annotations

from app.version import VERSION


def render_compliance(state: dict[str, object], width: int = 94) -> list[str]:
    audit=state["audit"]
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 7/8 COMPLIANCE",
        "="*width,
        f"Audit chain={'VALID' if audit.get('ok') else 'INVALID'} Entries={audit.get('entries',0)}",
        "-"*width,
        "PRODUCT: restricted goods, counterfeit, trademark, safety, electrical, battery, textile.",
        "TRADE: customs, dangerous goods, sanctions, export controls and destination restrictions.",
        "CANADA/QUEBEC: consumer-product screening, French-language readiness and tax categorization.",
        "PRIVACY: data minimization, PII encryption, retention, export, redaction and consent ledger.",
        "PAYMENTS: payment-card storage forbidden; supplier payment uses token reference only.",
        "MEDIA: reuse rights evidence and metadata scrubbing before Shopify attachment.",
        "-"*width,
        "Quarantined products cannot be published until every blocking finding is resolved.",
    ]
