from infrastructure.database.engine import Database
class ComplianceWebhookHandlers:
    def __init__(self,db: Database) -> None: self.db=db
    def customer_data_request(self,payload: dict[str,object]) -> None:
        self.db.insert_audit("customer_data_request","shopify",payload)
    def customer_redact(self,payload: dict[str,object]) -> None:
        customer_id=str(payload.get("customer",{}).get("id","")) if isinstance(payload.get("customer"),dict) else ""
        if customer_id: self.db.execute("UPDATE orders SET encrypted_shipping_address='' WHERE customer_id=?",(customer_id,))
        self.db.insert_audit("customer_redact","shopify",{"customer_id":customer_id})
    def shop_redact(self,payload: dict[str,object]) -> None:
        self.db.insert_audit("shop_redact","shopify",payload)
