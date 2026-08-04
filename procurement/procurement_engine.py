from __future__ import annotations
import json
from uuid import uuid4
from config.settings import Settings
from infrastructure.database.engine import Database,utcnow
from integrations.alibaba.client import AlibabaClient
from procurement.batch_builder import BatchBuilder
from procurement.threshold_manager import ThresholdManager
from procurement.payment_approval_gate import PaymentApprovalGate
from procurement.payment_orchestrator import PaymentOrchestrator
from domain.value_objects.idempotency_key import build_idempotency_key

class ProcurementEngine:
    def __init__(self,settings: Settings,db: Database,client: AlibabaClient) -> None:
        self.settings=settings; self.db=db; self.client=client
        self.builder=BatchBuilder(db)
        self.threshold=ThresholdManager(settings.alibaba_batch_threshold_cad,
                                        settings.alibaba_batch_max_age_minutes,
                                        settings.alibaba_batch_max_orders)
        self.gate=PaymentApprovalGate(db,settings.alibaba_require_manual_payment_approval)
        self.payments=PaymentOrchestrator(settings,db,client,self.gate)

    def accumulate_paid_orders(self) -> dict[str,object]:
        batch=self.builder.get_or_create_open_batch()
        for order in self.builder.ready_orders():
            self.builder.add_order(str(batch["id"]),str(order["id"]),"default",float(order["supplier_cost_cad"])+float(order["shipping_cost_cad"]))
        return self.db.query_one("SELECT * FROM batches WHERE id=?",(batch["id"],)) or batch

    def evaluate_batch(self,batch: dict[str,object]) -> dict[str,object]:
        decision=self.threshold.evaluate(float(batch["total_cad"]),str(batch["created_at"]),int(batch["order_count"]))
        if decision.ready and batch["status"]=="open":
            self.db.execute("UPDATE batches SET status='ready',updated_at=? WHERE id=?",(utcnow(),batch["id"]))
        return {"ready":decision.ready,"reason":decision.reason}

    async def submit_batch(self,batch_id: str) -> dict[str,object]:
        batch=self.db.query_one("SELECT * FROM batches WHERE id=?",(batch_id,))
        if not batch: raise KeyError(batch_id)
        orders=self.db.query("SELECT o.* FROM orders o JOIN batch_orders bo ON bo.order_id=o.id WHERE bo.batch_id=?",(batch_id,))
        if not orders: raise ValueError("Lot vide.")
        if self.settings.alibaba_require_manual_payment_approval and not self.gate.approved(batch_id):
            approval_id=self.gate.request(batch_id,float(batch["total_cad"]))
            self.db.execute("UPDATE batches SET status='approval_required',updated_at=? WHERE id=?",(utcnow(),batch_id))
            return {"status":"approval_required","approval_id":approval_id}
        supplier_orders=[]
        for order in orders:
            lines=self.db.query("SELECT * FROM order_lines WHERE order_id=?",(order["id"],))
            address={"encrypted_reference":order["encrypted_shipping_address"]}
            items=[{"product_id":line["supplier_product_id"],"sku_id":line["supplier_sku_id"],
                    "quantity":line["quantity"]} for line in lines]
            key=build_idempotency_key("supplier-order",batch_id,order["id"])
            if self.settings.app_dry_run:
                response={"order_id":"DRY-"+key[:16],"status":"created","dry_run":True}
            else:
                response=await self.client.create_buy_now_order(items,address,
                    f"Shopify {order['name']} / batch {batch_id}",key)
            external_id=str(response.get("order_id") or response.get("orderId") or response.get("id") or "")
            supplier_orders.append({"shopify_order":order["id"],"supplier_order_id":external_id,"response":response})
            self.db.execute("UPDATE batch_orders SET supplier_order_id=? WHERE batch_id=? AND order_id=?",
                            (external_id,batch_id,order["id"]))
            self.db.execute("UPDATE orders SET procurement_status='ordered',updated_at=? WHERE id=?",(utcnow(),order["id"]))
        self.db.execute("UPDATE batches SET status='submitted',external_ids_json=?,submitted_at=?,updated_at=? WHERE id=?",
                        (json.dumps([x["supplier_order_id"] for x in supplier_orders]),utcnow(),utcnow(),batch_id))
        payment_results=[]
        for supplier_order in supplier_orders:
            payment_results.append(await self.payments.pay(batch_id,supplier_order["supplier_order_id"],
                                                          float(batch["total_cad"])/len(supplier_orders),"CAD"))
        paid=all(p["status"] in {"paid","success","completed"} for p in payment_results)
        if paid:
            self.db.execute("UPDATE batches SET status='paid',paid_at=?,updated_at=? WHERE id=?",(utcnow(),utcnow(),batch_id))
        return {"status":"paid" if paid else "submitted","supplier_orders":supplier_orders,"payments":payment_results}
