from __future__ import annotations
import json
from decimal import Decimal
from uuid import uuid4
from infrastructure.database.engine import Database,utcnow
from integrations.shopify.mappers.order_mapper import map_shopify_order
from security.pii_vault import PIIVault
from finance.accounting_engine import AccountingEngine

class OrderIntakeWorkflow:
    def __init__(self,db: Database,vault: PIIVault,accounting: AccountingEngine) -> None:
        self.db=db; self.vault=vault; self.accounting=accounting
    async def execute(self,payload: dict[str,object]) -> dict[str,object]:
        order=map_shopify_order(payload)
        internal_id=str(uuid4()); existing=self.db.query_one("SELECT id FROM orders WHERE shopify_order_id=?",(order["shopify_order_id"],))
        if existing: internal_id=str(existing["id"])
        address=self.vault.store_address(order["shipping_address"]) if order["shipping_address"] else ""
        customer=order["customer"] if isinstance(order["customer"],dict) else {}
        self.db.execute("""INSERT INTO orders(id,shopify_order_id,name,customer_id,encrypted_shipping_address,currency,total_amount,
          revenue_cad,financial_status,fulfillment_status,payload_json,created_at,updated_at)
          VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
          ON CONFLICT(shopify_order_id) DO UPDATE SET financial_status=excluded.financial_status,
          fulfillment_status=excluded.fulfillment_status,payload_json=excluded.payload_json,updated_at=excluded.updated_at,
          encrypted_shipping_address=excluded.encrypted_shipping_address""",
          (internal_id,order["shopify_order_id"],order["name"],str(customer.get("id","")),address,order["currency"],float(order["total"]),
           float(order["total"]),order["financial_status"],order["fulfillment_status"],json.dumps(payload,ensure_ascii=False,default=str),utcnow(),utcnow()))
        for line in order["lines"]:
            self.db.execute("""INSERT INTO order_lines(id,order_id,shopify_line_id,shopify_variant_id,sku,title,quantity,unit_revenue_cad)
              VALUES(?,?,?,?,?,?,?,?)
              ON CONFLICT(order_id,shopify_line_id) DO UPDATE SET quantity=excluded.quantity,unit_revenue_cad=excluded.unit_revenue_cad""",
              (str(uuid4()),internal_id,line["id"],line["variant_id"],line["sku"],line["title"],line["quantity"],float(line["unit_price"])))
        if order["financial_status"]=="paid" and not self.db.get_value(f"accounted:sale:{internal_id}",False):
            self.accounting.recognize_sale(internal_id,float(order["total"])); self.db.set_value(f"accounted:sale:{internal_id}",True)
        return {"id":internal_id,"financial_status":order["financial_status"],"line_count":len(order["lines"])}
