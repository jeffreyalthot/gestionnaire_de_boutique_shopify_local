from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True, slots=True)
class SequenceDecision:
    process: bool
    stale: bool
    observed_at: str
    reason: str

class WebhookSequenceGuard:
    """Empêche un webhook plus ancien d'écraser un état plus récent d'une ressource."""
    def __init__(self) -> None:
        self._latest: dict[str, datetime] = {}

    @staticmethod
    def _parse(value: str) -> datetime:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    def evaluate(self, resource_key: str, triggered_at: str) -> SequenceDecision:
        if not resource_key or not triggered_at:
            return SequenceDecision(True, False, triggered_at, "Ordonnancement impossible; traitement conservateur.")
        try:
            observed = self._parse(triggered_at)
        except ValueError:
            return SequenceDecision(True, False, triggered_at, "Horodatage invalide; traitement conservateur.")
        previous = self._latest.get(resource_key)
        if previous is not None and observed < previous:
            return SequenceDecision(False, True, triggered_at, "Webhook antérieur à l'état déjà traité.")
        self._latest[resource_key] = observed
        return SequenceDecision(True, False, triggered_at, "Webhook courant.")
