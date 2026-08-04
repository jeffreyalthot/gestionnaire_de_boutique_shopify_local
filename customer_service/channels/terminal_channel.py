from __future__ import annotations

from typing import Callable


class TerminalChannel:
    def __init__(self, sink: Callable[[str], None]) -> None:
        self.sink = sink

    def send(self, ticket_id: str, message: str) -> dict[str, str]:
        text = " ".join(message.replace("\r", " ").replace("\n", " ").split())[:1000]
        self.sink(f"TICKET {ticket_id}: {text}")
        return {"status": "displayed", "ticket_id": ticket_id}
