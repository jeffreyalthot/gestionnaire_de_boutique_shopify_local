from __future__ import annotations
from typing import Any
async def readiness(container: Any) -> dict[str,object]:
    database=container.db.health();health=await container.health.collect() if hasattr(container,"health") else {"ok":bool(database.get("ok")),"status":"unknown"};capabilities=container.capabilities.snapshot() if hasattr(container,"capabilities") else {}
    blockers=[]
    if not database.get("ok"):blockers.append("database")
    if not health.get("ok"):blockers.extend(health.get("critical_failures",()))
    if not container.settings.app_dry_run:
        if not container.settings.live_shopify_ready:blockers.append("shopify_configuration")
        if not container.settings.live_alibaba_ready:blockers.append("alibaba_configuration")
    return {"ready":not blockers,"database":database,"health":health,"capabilities":capabilities,"dry_run":container.settings.app_dry_run,"blockers":tuple(dict.fromkeys(blockers))}
