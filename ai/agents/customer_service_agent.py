from ai.agents.base_agent import PolicyAwareAgent


class CustomerServiceAgent(PolicyAwareAgent):
    description = 'Classe et prépare les réponses client.'
    positive_signals = ('intent_confidence', 'template_quality')
    negative_signals = ('sentiment_risk', 'sla_risk')
    hard_block_signals = ('legal_threat', 'payment_data_present')

    def prepare_context(self, context):
        value=dict(context); age=float(value.get("ticket_age_hours",0) or 0); sla=float(value.get("sla_hours",24) or 24)
        value.setdefault("sla_risk", min(1.0,age/max(sla,1.0)))
        value.setdefault("intent_confidence", float(value.get("classification_confidence",.5) or .5))
        value.setdefault("template_quality", 1.0 if value.get("template_id") else .4)
        message=str(value.get("message","")).lower(); value.setdefault("legal_threat", any(x in message for x in ("avocat","lawsuit","legal action")))
        return value

