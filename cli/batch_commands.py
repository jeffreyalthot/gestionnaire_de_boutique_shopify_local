from __future__ import annotations
from cli.base_commands import BaseCommands

class BatchCommands(BaseCommands):
    resource='batches'
    def action_list(self,limit: int=50,**_):return self.result("list",self.container.db.query("SELECT * FROM batches ORDER BY created_at DESC LIMIT ?",(max(1,min(int(limit),500)),)))
    def action_evaluate(self,**_):
        batch=self.container.procurement.accumulate_paid_orders();return self.result("evaluate",{"batch":batch,"decision":self.container.procurement.evaluate_batch(batch)})
