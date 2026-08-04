from ai.agents.base_agent import PolicyAwareAgent


class AccountingAgent(PolicyAwareAgent):
    description = 'Détecte les écarts financiers.'
    positive_signals = ('reconciliation_quality', 'ledger_integrity')
    negative_signals = ('variance_ratio', 'unmatched_ratio')
    hard_block_signals = ('ledger_unbalanced', 'missing_payout')

    def prepare_context(self, context):
        value = dict(context)
        debit = float(value.get("ledger_debit", 0) or 0); credit = float(value.get("ledger_credit", 0) or 0)
        total = max(abs(debit), abs(credit), 1.0)
        value.setdefault("ledger_integrity", max(0.0, 1.0 - abs(debit-credit)/total))
        value.setdefault("variance_ratio", min(1.0, abs(float(value.get("expected",0) or 0)-float(value.get("actual",0) or 0))/max(abs(float(value.get("expected",0) or 0)),1.0)))
        value.setdefault("reconciliation_quality", 1.0-float(value.get("unmatched_ratio",0) or 0))
        value.setdefault("ledger_unbalanced", abs(debit-credit) >= .01)
        return value

