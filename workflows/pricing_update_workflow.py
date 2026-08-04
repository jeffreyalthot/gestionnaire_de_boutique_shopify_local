from workflows.base_workflow import ServiceWorkflow


class PricingUpdateWorkflow(ServiceWorkflow):
    name = 'pricing_update'
    method_candidates = ('reprice', 'update_prices', 'execute', 'run')
