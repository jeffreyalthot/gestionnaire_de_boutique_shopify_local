from __future__ import annotations

from typing import Any, Callable


class EmailChannel:
    """Adaptateur injecté: ne stocke jamais les identifiants SMTP dans l'objet."""

    def __init__(self, sender: Callable[[str, str, str], Any]) -> None:
        self.sender = sender

    async def send(self, recipient_reference: str, subject: str, body: str) -> dict[str, object]:
        result = self.sender(recipient_reference, subject[:200], body[:10000])
        if hasattr(result, "__await__"):
            result = await result
        return {"status": "sent", "provider_result": result}
