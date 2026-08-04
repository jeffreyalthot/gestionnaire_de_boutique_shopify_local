from __future__ import annotations
from cli.base_commands import BaseCommands

class AiCommands(BaseCommands):
    resource='ai'
    def action_models(self,**_):return self.result("models",self.container.ai.status())
    def action_decisions(self,limit: int=50,**_):return self.result("decisions",self.container.db.query("SELECT * FROM ai_decisions ORDER BY created_at DESC LIMIT ?",(max(1,min(int(limit),500)),)))
