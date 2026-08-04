from __future__ import annotations

from app.version import VERSION


def render_system(state: dict[str, object], width: int = 94) -> list[str]:
    runtime=state["runtime"]; r=runtime["resource"]; q=state["queue"]; integrations=state.get("integration_runtime",{})
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 8/8 SYSTEM",
        "="*width,
        f"CPU={runtime['cpu_percent']:.1f}% RAM={runtime['rss_mb']:.1f}/{r['budget']['max_rss_mb']:.0f} MB Profile={runtime['profile']}",
        f"Workers={r['budget']['worker_threads']} HTTP concurrency={r['budget']['max_http_concurrency']} Heavy/cycle={r['budget']['max_heavy_operations_per_cycle']}",
        f"Queue pending={q.get('pending',0)} leased={q.get('leased',0)} completed={q.get('completed',0)} dead={q.get('dead',0)} cancelled={q.get('cancelled',0)}",
        f"Webhook handlers={integrations.get('webhook_handlers',{}).get('count',0)} Sales channels={len(integrations.get('sales_channels',{}))}",
        "-"*width,
        "RESOURCE GOVERNOR: memory ceiling, queue backpressure, bounded workers and one heavy task/cycle.",
        "DATABASE: SQLite WAL, busy timeout, integrity check, atomic writes, backup and lease recovery.",
        "NETWORK: timeout, retry/backoff, rate limiting, concurrency 2 and request correlation IDs.",
        "TERMINAL: alternate screen, fixed rows, differential redraw, event ring and single output owner.",
        "RECOVERY: expired lease reset, dead-letter queue, operation checkpoint and idempotent replay.",
        "-"*width,
        f"Current cycle={r['cycle_id']} Heavy used={r['heavy_used']} Memory OK={r['within_memory_budget']} CPU OK={r['within_cpu_budget']}",
    ]
