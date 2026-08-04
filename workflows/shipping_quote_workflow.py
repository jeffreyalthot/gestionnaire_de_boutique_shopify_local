from workflows.base_workflow import ServiceWorkflow


class ShippingQuoteWorkflow(ServiceWorkflow):
    name = 'shipping_quote'
    method_candidates = ('quote', 'get_quote', 'execute', 'run')
