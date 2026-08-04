from __future__ import annotations

from app.version import VERSION


def render_marketing(state: dict[str, object], width: int = 94) -> list[str]:
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 6/8 MARKETING",
        "="*width,
        "SEO: title, description, handle, alt text, structured data and internal links.",
        "MERCHANDISING: collections, tags, bundles, upsell, cross-sell and variant display rules.",
        "DISCOUNTS: minimum-margin guard, budget ceiling, start/end dates and conflict detection.",
        "CAMPAIGNS: budget allocation by channel, audience segment, cadence and attribution snapshot.",
        "EMAIL FLOWS: abandoned checkout, post-purchase, replenishment and win-back plans.",
        "CONTENT: brand-voice policy, product-content audit, blog/calendar and page maintenance.",
        "-"*width,
        "No campaign or discount is activated live without capability, budget and policy approval.",
    ]
