from integrations.alibaba.client import AlibabaClient
class ProductRepository:
    def __init__(self,client: AlibabaClient) -> None: self.client=client
    @property
    def resource(self) -> str: return "product"
