from ai.agents.base_agent import PolicyAwareAgent


class InventoryAgent(PolicyAwareAgent):
    description = 'Détecte pénuries et stock obsolète.'
    positive_signals = ('inventory_accuracy', 'supplier_availability')
    negative_signals = ('stockout_risk', 'stale_stock_ratio')
    hard_block_signals = ('negative_inventory', 'reservation_drift')

    def prepare_context(self, context):
        value=dict(context); on_hand=int(value.get("on_hand",0) or 0); reserved=int(value.get("reserved",0) or 0); demand=float(value.get("daily_demand",0) or 0)
        available=on_hand-reserved; value.setdefault("negative_inventory", available<0)
        value.setdefault("stockout_risk", min(1.0,demand/max(available,1)) if demand>0 else 0.0)
        value.setdefault("inventory_accuracy", max(0.0,1.0-float(value.get("drift_ratio",0) or 0)))
        return value

