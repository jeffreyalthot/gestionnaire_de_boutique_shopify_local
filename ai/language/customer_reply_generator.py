from __future__ import annotations

from ai.language.template_engine import TemplateEngine
from ai.language.text_sanitizer import sanitize


class CustomerReplyGenerator:
    """Deterministic customer-service replies with no external model required."""

    def __init__(self, engine: TemplateEngine | None = None) -> None:
        self.engine = engine or TemplateEngine()
        templates = {
            "tracking": ("Bonjour $name, votre commande est expédiée. Numéro de suivi : $tracking_number. Suivi : $url", ("name", "tracking_number", "url")),
            "delay": ("Bonjour $name, nous vous informons que la livraison est maintenant prévue pour le $new_date. Nous suivons activement l'expédition.", ("name", "new_date")),
            "refund": ("Bonjour $name, votre remboursement de $amount a été autorisé. Le délai bancaire estimé est de $business_days jours ouvrables.", ("name", "amount", "business_days")),
            "cancelled": ("Bonjour $name, la commande $order_name a été annulée. $refund_sentence", ("name", "order_name", "refund_sentence")),
            "missing_item": ("Bonjour $name, nous sommes désolés qu'un article manque dans la commande $order_name. Dossier : $ticket_id. Nous vérifions l'expédition avec le fournisseur.", ("name", "order_name", "ticket_id")),
            "damaged_item": ("Bonjour $name, nous sommes désolés que l'article soit arrivé endommagé. Dossier : $ticket_id. Veuillez conserver l'emballage pendant l'analyse.", ("name", "ticket_id")),
            "wrong_item": ("Bonjour $name, nous avons ouvert le dossier $ticket_id pour l'article incorrect reçu dans la commande $order_name.", ("name", "ticket_id", "order_name")),
        }
        for name, (template, required) in templates.items():
            if name not in self.engine.names():
                self.engine.register(name, template, required=required)

    @staticmethod
    def _name(name: str) -> str:
        return sanitize(name, 100) or "client"

    def tracking(self, name: str, tracking_number: str, url: str) -> str:
        return self.engine.render_named("tracking", {
            "name": self._name(name),
            "tracking_number": sanitize(tracking_number, 120),
            "url": sanitize(url, 500),
        })

    def delay(self, name: str, new_date: str) -> str:
        return self.engine.render_named("delay", {"name": self._name(name), "new_date": sanitize(new_date, 100)})

    def refund(self, name: str, amount: str, business_days: int = 10) -> str:
        return self.engine.render_named("refund", {
            "name": self._name(name), "amount": sanitize(amount, 60),
            "business_days": max(1, min(int(business_days), 60)),
        })

    def cancelled(self, name: str, order_name: str, *, refunded: bool) -> str:
        sentence = "Le remboursement a été lancé." if refunded else "Aucun paiement n'a été capturé."
        return self.engine.render_named("cancelled", {
            "name": self._name(name), "order_name": sanitize(order_name, 80),
            "refund_sentence": sentence,
        })

    def missing_item(self, name: str, order_name: str, ticket_id: str) -> str:
        return self.engine.render_named("missing_item", {
            "name": self._name(name), "order_name": sanitize(order_name, 80),
            "ticket_id": sanitize(ticket_id, 80),
        })

    def damaged_item(self, name: str, ticket_id: str) -> str:
        return self.engine.render_named("damaged_item", {
            "name": self._name(name), "ticket_id": sanitize(ticket_id, 80),
        })

    def wrong_item(self, name: str, order_name: str, ticket_id: str) -> str:
        return self.engine.render_named("wrong_item", {
            "name": self._name(name), "order_name": sanitize(order_name, 80),
            "ticket_id": sanitize(ticket_id, 80),
        })
