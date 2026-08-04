from __future__ import annotations

from app.version import VERSION

from dashboard.pages.common import money, section


def render_executive(state: dict[str, object], width: int = 94) -> list[str]:
    counts = state["counts"]; finance = state["finance"]; runtime = state["runtime"]
    automation = state["automation"]; api = state["api"]; queue = state["queue"]
    pending = int(queue.get("pending", 0)) + int(queue.get("leased", 0))
    return [
        f"SHOPIFY - ALIBABA AUTOMATION MANAGER {VERSION} | PAGE 1/8 EXECUTIVE",
        "=" * width,
        f"MODE {state['mode']['name']:<18} PROFILE {runtime['profile']:<14} UPTIME {int(runtime['uptime_seconds']):>8}s",
        f"CPU {runtime['cpu_percent']:>6.1f}%  RAM {runtime['rss_mb']:>7.1f}/{runtime['resource']['budget']['max_rss_mb']:.0f} MB  QUEUE {pending:>7}",
        f"SERVICES SQLite={'OK' if api['database']['ok'] else 'ERROR'} Shopify={'READY' if api['shopify_ready'] else 'DRY'} Alibaba={'READY' if api['alibaba_ready'] else 'DRY'} Payment={'READY' if api['payment_ready'] else 'GATED'}",
        *section("COMMERCE", width),
        f"Orders={counts.get('orders',0)} Paid={counts.get('paid_orders',0)} Procurement={counts.get('pending_procurement',0)} Products={counts.get('products',0)}",
        f"Open batches={counts.get('open_batches',0)} Pending tasks={counts.get('pending_tasks',0)} Failed tasks={counts.get('failed_tasks',0)}",
        *section("FINANCE", width),
        f"Revenue {money(finance.get('revenue')):<22} Supplier {money(finance.get('supplier_cost')):<22}",
        f"Shipping {money(finance.get('shipping')):<21} Fees {money(finance.get('fees')):<26}",
        f"Profit {money(finance.get('profit'))}",
        *section("AUTOMATION", width),
        f"Phase={automation['phase']} Cycle={automation['cycle_id'][:20]} Cycles={automation['cycles']}",
        f"Planned={automation['planned']} Accepted={automation['accepted']} Deferred={automation['deferred']} Rejected={automation['rejected']}",
        f"Completed={automation['completed']} Failed={automation['failed']} Retried={automation['retried']} Compensated={automation['compensated']}",
        f"Last action={automation['last_action']}",
    ]
