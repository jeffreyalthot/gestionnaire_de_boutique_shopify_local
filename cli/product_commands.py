from __future__ import annotations
from cli.base_commands import BaseCommands

class ProductCommands(BaseCommands):
    resource='products'
    def action_candidates(self,limit: int=100,**_):return self.result("candidates",self.container.db.query("SELECT * FROM products WHERE status IN ('candidate','draft') ORDER BY score DESC LIMIT ?",(max(1,min(int(limit),1000)),)))
    def action_active(self,limit: int=100,**_):return self.result("active",self.container.db.query("SELECT * FROM products WHERE status IN ('active','published') ORDER BY updated_at DESC LIMIT ?",(max(1,min(int(limit),1000)),)))
