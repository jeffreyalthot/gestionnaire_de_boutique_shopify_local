from __future__ import annotations

from typing import Any

from app.version import VERSION


def build_startup_banner(settings: Any, *, version: str = VERSION) -> tuple[str, ...]:
    mode = "DRY-RUN" if settings.app_dry_run else "SUPERVISED-LIVE"
    return (
        "=" * 78,
        f" SHOPIFY + ALIBABA TERMINAL ORCHESTRATOR {version}",
        f" MODE={mode} PROFILE={settings.runtime_profile} CPU<=2 HTTP<={settings.max_concurrent_http_requests}",
        " CONSOLE OWNER=terminal | FIXED ROWS | SQLITE DURABLE QUEUES | AUDIT CHAIN",
        "=" * 78,
    )
