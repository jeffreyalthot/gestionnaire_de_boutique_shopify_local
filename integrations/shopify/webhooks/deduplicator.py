from infrastructure.database.engine import Database
class WebhookDeduplicator:
    def __init__(self,db: Database) -> None: self.db=db
    def register(self,webhook_id: str,topic: str,shop: str,payload: dict[str,object]) -> bool:
        return self.db.insert_event("shopify",topic,webhook_id,payload,shop)
