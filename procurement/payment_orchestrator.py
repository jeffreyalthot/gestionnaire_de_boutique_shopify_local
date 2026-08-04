from __future__ import annotations
import json
from uuid import uuid4
from config.settings import Settings
from infrastructure.database.engine import Database,utcnow
from integrations.alibaba.client import AlibabaClient
from procurement.payment_approval_gate import PaymentApprovalGate
from security.pci_guard import reject_payment_card_data

class PaymentOrchestrator:
    def __init__(self,settings: Settings,db: Database,client: AlibabaClient,gate: PaymentApprovalGate) -> None:
        self.settings=settings; self.db=db; self.client=client; self.gate=gate
    async def pay(self,batch_id: str,supplier_order_id: str,amount: float,currency: str) -> dict[str,object]:
        reject_payment_card_data({"payment_token_reference":self.settings.alibaba_payment_token_reference.get_secret_value()})
        if not self.gate.approved(batch_id):
            approval_id=self.gate.request(batch_id,amount)
            return {"status":"approval_required","approval_id":approval_id}
        if self.settings.app_dry_run:
            result={"status":"paid","dry_run":True,"order_id":supplier_order_id}
        else:
            if not self.settings.live_payment_ready: raise RuntimeError("Paiement Alibaba réel non configuré.")
            result=await self.client.pay_dropshipping_order(
                supplier_order_id,self.settings.alibaba_payment_token_reference.get_secret_value())
        payment_id=str(uuid4()); status=str(result.get("status") or result.get("pay_status") or "submitted").lower()
        self.db.execute("INSERT INTO payments(id,batch_id,supplier_order_id,amount,currency,status,response_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (payment_id,batch_id,supplier_order_id,amount,currency,status,json.dumps(result,ensure_ascii=False,default=str),utcnow(),utcnow()))
        return {"payment_id":payment_id,"status":status,"response":result}
