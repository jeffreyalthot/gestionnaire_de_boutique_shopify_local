from __future__ import annotations


class PublicationPlanner:
    def plan(self, *, validation: dict[str, object], channels: list[str], markets: list[str],
             approval_granted: bool = False) -> dict[str, object]:
        if not validation.get("passed"):
            return {"status": "blocked", "reason": "validation_failed", "failures": validation.get("failures", ())}
        if not approval_granted:
            return {"status": "awaiting_approval", "reason": "publication_approval_required"}
        return {"status": "ready", "channels": tuple(sorted(set(channels))), "markets": tuple(sorted(set(markets)))}
