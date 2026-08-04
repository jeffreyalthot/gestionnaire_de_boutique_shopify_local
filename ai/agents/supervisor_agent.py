from ai.agents.base_agent import PolicyAwareAgent


class SupervisorAgent(PolicyAwareAgent):
    description = "Coordonne les décisions et applique les politiques d'autonomie."
    positive_signals = ('policy_score', 'consensus_score', 'audit_completeness')
    negative_signals = ('aggregate_risk', 'exception_rate')
    hard_block_signals = ('lockdown', 'policy_violation')

    def prepare_context(self, context):
        value=dict(context); decisions=list(value.get("decisions",[]) or [])
        if decisions:
            approvals=sum(str(d.get("decision","")).lower()=="approve" for d in decisions if isinstance(d,dict)); value.setdefault("consensus_score", approvals/max(len(decisions),1))
            value.setdefault("aggregate_risk", max((1.0-float(d.get("score",.5) or .5) for d in decisions if isinstance(d,dict)),default=.5))
        value.setdefault("audit_completeness", 1.0 if value.get("audit_id") else .4); return value

