from ai.agents.base_agent import PolicyAwareAgent


class DemandAgent(PolicyAwareAgent):
    description = 'Prévoit la demande avec apprentissage incrémental.'
    positive_signals = ('forecast_confidence', 'history_quality')
    negative_signals = ('forecast_error', 'stockout_bias')
    hard_block_signals = ('insufficient_history',)

    def prepare_context(self, context):
        value=dict(context); history=list(value.get("history",[]) or []); n=len(history)
        value.setdefault("history_quality", min(1.0,n/90.0)); value.setdefault("forecast_confidence", min(.95,.35+n/180.0))
        value.setdefault("insufficient_history", n<7 and "forecast_confidence" not in context)
        if value.get("actual") is not None and value.get("forecast") is not None:
            value.setdefault("forecast_error", min(1.0,abs(float(value["actual"])-float(value["forecast"]))/max(abs(float(value["actual"])),1.0)))
        return value

