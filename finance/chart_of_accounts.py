from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class Account:
    code: str
    name: str
    category: str
    normal_balance: str

    def as_dict(self):
        return asdict(self)


DEFAULT_ACCOUNTS = (
    Account("1000", "Cash and receivables", "asset", "debit"),
    Account("1100", "Inventory in transit", "asset", "debit"),
    Account("2000", "Supplier payable", "liability", "credit"),
    Account("2100", "Tax reserve", "liability", "credit"),
    Account("2200", "Refund reserve", "liability", "credit"),
    Account("4000", "Sales revenue", "revenue", "credit"),
    Account("4010", "Sales returns", "revenue", "debit"),
    Account("5000", "Cost of goods sold", "expense", "debit"),
    Account("5100", "Shipping expense", "expense", "debit"),
    Account("5200", "Platform fees", "expense", "debit"),
    Account("5300", "Marketing expense", "expense", "debit"),
    Account("5400", "Chargeback expense", "expense", "debit"),
)


class ChartOfAccounts:
    def __init__(self, accounts: tuple[Account, ...] = DEFAULT_ACCOUNTS) -> None:
        self._accounts = {account.code: account for account in accounts}

    def get(self, code: str) -> Account:
        return self._accounts[code]

    def all(self) -> tuple[Account, ...]:
        return tuple(self._accounts[key] for key in sorted(self._accounts))
