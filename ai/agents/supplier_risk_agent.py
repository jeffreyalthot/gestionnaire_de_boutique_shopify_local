from ai.agents.base_agent import PolicyAwareAgent


class SupplierRiskAgent(PolicyAwareAgent):
    description = 'Évalue le risque fournisseur.'
    positive_signals = ('verification_score', 'response_score', 'quality_score')
    negative_signals = ('dispute_rate', 'late_rate', 'price_volatility')
    hard_block_signals = ('sanctions_match', 'counterfeit_history', 'trade_assurance_missing')

    def prepare_context(self, context):
        value=dict(context); orders=max(1,int(value.get("orders",0) or 0)); disputes=int(value.get("disputes",0) or 0); late=int(value.get("late_orders",0) or 0)
        value.setdefault("dispute_rate", min(1.0,disputes/orders)); value.setdefault("late_rate", min(1.0,late/orders))
        value.setdefault("verification_score", 1.0 if value.get("verified") else .35); value.setdefault("trade_assurance_missing", not bool(value.get("trade_assurance",True))); return value

