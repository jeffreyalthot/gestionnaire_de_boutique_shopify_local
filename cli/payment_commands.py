from __future__ import annotations
from cli.base_commands import BaseCommands

class PaymentCommands(BaseCommands):
    resource='payments'
    def action_summary(self,**_):return self.result("summary",self.container.db.query("SELECT status,currency,COUNT(*) count,ROUND(SUM(amount),2) amount FROM payments GROUP BY status,currency"))
    def action_pending(self,**_):return self.result("pending",self.container.db.query("SELECT * FROM payments WHERE status IN ('pending','review','retry') ORDER BY created_at"))
