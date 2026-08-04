from integrations.alibaba.client import AlibabaClient
class OrderRepository:
    def __init__(self,client: AlibabaClient) -> None: self.client=client
    @property
    def resource(self) -> str: return "order"
