from ai.agents.base_agent import PolicyAwareAgent


class AnomalyAgent(PolicyAwareAgent):
    description = 'Détecte les valeurs anormales.'
    positive_signals = ('data_quality', 'sample_confidence')
    negative_signals = ('anomaly_score', 'drift_score')
    hard_block_signals = ('corrupt_input',)

    def prepare_context(self, context):
        value=dict(context); samples=int(value.get("samples",0) or 0)
        value.setdefault("sample_confidence", min(1.0, samples/50.0))
        missing=float(value.get("missing_ratio",0) or 0); value.setdefault("data_quality", max(0.0,1.0-missing))
        value.setdefault("corrupt_input", missing>=1.0 or bool(value.get("parse_error")))
        return value

