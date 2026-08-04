from __future__ import annotations
from cli.base_commands import BaseCommands

class MaintenanceCommands(BaseCommands):
    resource='maintenance'
    def action_health(self,**_):return self.result("health",self.container.db.health())
    def action_recover(self,**_):return self.result("recover",self.container.runtime_coordinator.recover())
    def action_queue(self,**_):return self.result("queue",{"stats":self.container.queue.stats(),"queues":self.container.queue.stats_by_queue()})
