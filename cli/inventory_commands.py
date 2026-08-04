from __future__ import annotations
from cli.base_commands import BaseCommands

class InventoryCommands(BaseCommands):
    resource='inventory'
    def action_low_stock(self,limit: int=100,**_):return self.result("low_stock",self.container.db.query("SELECT *,on_hand-reserved available FROM inventory_positions WHERE on_hand-reserved<=safety_stock ORDER BY available LIMIT ?",(max(1,min(int(limit),1000)),)))
    def action_summary(self,**_):return self.result("summary",{"positions":self.container.db.scalar("SELECT COUNT(*) FROM inventory_positions",default=0),"reserved":self.container.db.scalar("SELECT COALESCE(SUM(reserved),0) FROM inventory_positions",default=0)})
