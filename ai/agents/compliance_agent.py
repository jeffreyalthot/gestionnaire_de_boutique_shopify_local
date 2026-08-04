from ai.agents.base_agent import PolicyAwareAgent


class ComplianceAgent(PolicyAwareAgent):
    description = 'Bloque les produits et actions non conformes.'
    positive_signals = ('compliance_score', 'evidence_score')
    negative_signals = ('restriction_risk', 'ip_risk')
    hard_block_signals = ('restricted_product', 'sanctions_match', 'counterfeit_risk')

    def prepare_context(self, context):
        value=dict(context); findings=list(value.get("findings",[]) or [])
        blockers=sum(str(f.get("severity","")).lower() in {"block","critical"} for f in findings if isinstance(f,dict))
        warnings=sum(str(f.get("severity","")).lower() in {"warning","high"} for f in findings if isinstance(f,dict))
        value.setdefault("compliance_score", max(0.0,1.0-(blockers*0.5+warnings*0.1)))
        value.setdefault("evidence_score", min(1.0,float(value.get("evidence_count",0) or 0)/5.0))
        value.setdefault("restricted_product", blockers>0)
        return value

