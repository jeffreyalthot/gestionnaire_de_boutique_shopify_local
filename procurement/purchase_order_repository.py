from procurement.purchase_intent_repository import PurchaseIntentRepository


class PurchaseOrderRepository(PurchaseIntentRepository):
    def pending(self, limit: int=100) -> list[dict[str,object]]:
        return self.db.query("SELECT * FROM purchase_intents WHERE status IN ('planned','approved','retry') ORDER BY created_at LIMIT ?",(max(1,min(limit,500)),))
