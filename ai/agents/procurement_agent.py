from ai.agents.base_agent import PolicyAwareAgent


class ProcurementAgent(PolicyAwareAgent):
    description = "Priorise les lots d'approvisionnement."
    positive_signals = ('supplier_score', 'stock_confidence', 'margin_score')
    negative_signals = ('lead_time_risk', 'cash_exposure')
    hard_block_signals = ('supplier_blocked', 'budget_exceeded')

    def prepare_context(self, context):
        value=dict(context); amount=float(value.get("amount_cad",0) or 0); budget=float(value.get("available_budget_cad",0) or 0)
        value.setdefault("cash_exposure", min(1.0,amount/max(budget,1.0))); value.setdefault("budget_exceeded", amount>budget if budget>=0 else True)
        value.setdefault("financial_action", amount>0); value.setdefault("stock_confidence", float(value.get("inventory_confidence",.5) or .5)); return value

