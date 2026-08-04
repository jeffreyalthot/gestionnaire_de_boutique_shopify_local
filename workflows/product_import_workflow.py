from workflows.base_workflow import ServiceWorkflow


class ProductImportWorkflow(ServiceWorkflow):
    name = 'product_import'
    method_candidates = ('import_product', 'import_products', 'execute', 'run')
