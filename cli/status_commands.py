from __future__ import annotations
from cli.base_commands import BaseCommands

class StatusCommands(BaseCommands):
    resource='status'
    def action_services(self,**_):return self.result("services",self.container.service_registry.snapshot())
    def action_capabilities(self,**_):return self.result("capabilities",self.container.capabilities.snapshot())
