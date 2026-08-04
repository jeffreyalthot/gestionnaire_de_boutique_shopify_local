from __future__ import annotations
from cli.base_commands import BaseCommands

class EmergencyCommands(BaseCommands):
    resource='emergency'
    def action_state(self,**_):return self.result("state",self.container.lockdown.snapshot())
    def action_activate(self,reason: str="operator",**_):
        self.container.lockdown.activate(reason);return self.result("activate",self.container.lockdown.snapshot())
    def action_release(self,approved: bool=False,**_):
        if not approved:return self.result("release",{},False,"confirmation requise")
        self.container.lockdown.release();return self.result("release",self.container.lockdown.snapshot())
