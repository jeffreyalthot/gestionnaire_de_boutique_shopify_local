from ai.agents.base_agent import PolicyAwareAgent


class OrderRiskAgent(PolicyAwareAgent):
    description = 'Classe le risque des commandes.'
    positive_signals = ('identity_confidence', 'address_quality')
    negative_signals = ('fraud_score', 'velocity_score', 'chargeback_risk')
    hard_block_signals = ('payment_mismatch', 'blocked_country', 'fraud_confirmed')

    def prepare_context(self, context):
        value=dict(context); amount=float(value.get("amount",0) or 0); velocity=int(value.get("orders_last_hour",0) or 0)
        value.setdefault("velocity_score", min(1.0,velocity/5.0)); value.setdefault("fraud_score", min(1.0,float(value.get("risk_points",0) or 0)/100.0))
        value.setdefault("identity_confidence", 1.0 if value.get("customer_id") else .35); value.setdefault("address_quality", float(value.get("address_score",.5) or .5))
        value.setdefault("financial_action", amount>0); return value

