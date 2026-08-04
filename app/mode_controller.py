from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeMode:
    name: str
    external_mutations: bool
    financial_actions: bool
    automatic_approvals: bool


class ModeController:
    def __init__(self, dry_run: bool) -> None:
        self.current = RuntimeMode("dry_run" if dry_run else "supervised_live", not dry_run, not dry_run, False)

    def snapshot(self) -> dict[str, object]:
        return {"name": self.current.name, "external_mutations": self.current.external_mutations, "financial_actions": self.current.financial_actions, "automatic_approvals": self.current.automatic_approvals}
