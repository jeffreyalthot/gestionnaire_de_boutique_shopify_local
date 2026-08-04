from __future__ import annotations

import json
from typing import Any

from customer_service.ticket import Ticket
from infrastructure.database.engine import utcnow


class TicketRepository:
    def __init__(self, db: Any) -> None:
        self.db = db

    def save(self, ticket: Ticket, context: dict[str, object] | None = None) -> str:
        self.db.execute(
            "INSERT INTO customer_tickets(id,order_id,customer_id,category,priority,status,subject,context_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (ticket.id, ticket.order_id, ticket.customer_id, ticket.category, ticket.priority, ticket.status, ticket.subject, json.dumps(context or {}, ensure_ascii=False), ticket.created_at, utcnow()),
        )
        return ticket.id
