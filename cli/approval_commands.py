from __future__ import annotations
from cli.base_commands import BaseCommands

class ApprovalCommands(BaseCommands):
    resource='approvals'
    def action_pending(self,limit: int=50,**_):return self.result("pending",self.container.db.query("SELECT * FROM approvals WHERE status='pending' ORDER BY created_at LIMIT ?",(max(1,min(int(limit),500)),)))
