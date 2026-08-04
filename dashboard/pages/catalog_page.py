from __future__ import annotations

from app.version import VERSION


def render_catalog(state: dict[str, object], width: int = 94) -> list[str]:
    counts=state["counts"]; automation=state["automation"]; queue=state["queue"]
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 2/8 CATALOG",
        "="*width,
        f"Products total={counts.get('products',0)} Active={counts.get('active_products',0)}",
        f"Discovery queue={queue.get('pending',0)} Current operation={automation['last_action']}",
        "-"*width,
        "PIPELINE: Alibaba search -> dedup -> supplier score -> margin -> compliance -> media -> Shopify",
        "Discovery uses bounded pages and candidate limits; bulk data is streamed as JSONL.",
        "Media guard: public HTTP(S), allowlist optional, no credentials, no private/loopback addresses.",
        "Media validation: content magic, MIME, byte ceiling, dimensions, rights evidence, SHA-256 dedup.",
        "Product qualification: demand, competition, margin, supplier, quality, shipping, return risk.",
        "Publication remains approval-gated in live mode and simulated in dry-run mode.",
        "-"*width,
        "CATALOG STATES: candidate | qualified | quarantined | draft | active | paused | archived",
        "FAILURES: rights_unverified | compliance_block | low_margin | supplier_risk | invalid_media",
        "RECOVERY: idempotent import keys, media manifest, reconciliation checkpoints, compensating unpublish",
    ]
