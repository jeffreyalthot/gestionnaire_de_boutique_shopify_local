from ai.agents.base_agent import PolicyAwareAgent


class ShippingAgent(PolicyAwareAgent):
    description = 'Sélectionne les options de livraison.'
    positive_signals = ('tracking_quality', 'carrier_score', 'delivery_confidence')
    negative_signals = ('delay_risk', 'damage_risk')
    hard_block_signals = ('undeliverable_address', 'dangerous_goods_block')

    def prepare_context(self, context):
        value=dict(context); days=float(value.get("estimated_days",30) or 30); max_days=float(value.get("maximum_days",30) or 30)
        value.setdefault("delivery_confidence", max(0.0,1.0-days/max(max_days,1.0))); value.setdefault("delay_risk", min(1.0,days/max(max_days,1.0)))
        value.setdefault("tracking_quality", 1.0 if value.get("tracking_supported") else .25); return value

