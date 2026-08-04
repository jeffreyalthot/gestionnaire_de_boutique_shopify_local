from fulfillment.tracking_sync import TrackingSync
class TrackingSyncWorkflow:
    def __init__(self,sync: TrackingSync) -> None: self.sync=sync
    async def execute(self,shipment: dict[str,object]) -> dict[str,object]: return await self.sync.sync(shipment)
