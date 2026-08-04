from __future__ import annotations
from cli.base_commands import BaseCommands

class ReconciliationCommands(BaseCommands):
    resource='reconciliation'
    def action_state(self,**_):return self.result("state",{"finance":self.container.db.financial_snapshot(),"queue":self.container.queue.stats(),"audit":self.container.db.verify_audit_chain()})
    def action_run(self,**_):return self.result("run",self.container.runtime_coordinator.recover())
