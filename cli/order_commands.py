from __future__ import annotations
from cli.base_commands import BaseCommands

class OrderCommands(BaseCommands):
    resource='orders'
    def action_list(self,status: str="",limit: int=50,**_):
        if status:return self.result("list",self.container.db.query("SELECT * FROM orders WHERE financial_status=? OR fulfillment_status=? OR procurement_status=? ORDER BY created_at DESC LIMIT ?",(status,status,status,max(1,min(int(limit),500)))))
        return self.result("list",self.container.db.query("SELECT * FROM orders ORDER BY created_at DESC LIMIT ?",(max(1,min(int(limit),500)),)))
    def action_exceptions(self,**_):return self.result("exceptions",self.container.db.query("SELECT * FROM orders WHERE risk_level IN ('high','critical') OR procurement_status IN ('failed','blocked','retry') ORDER BY updated_at DESC LIMIT 200"))
