from fastapi import APIRouter,Depends,Query
from api.operator_auth import OperatorAuthorizer
from infrastructure.queue.dead_letter_queue import DeadLetterQueue

def router_for(container):
    router=APIRouter(prefix="/queues",tags=["queues"]);auth=OperatorAuthorizer(container.settings);dead=DeadLetterQueue(container.db)
    @router.get("")
    async def stats():return {"stats":container.queue.stats(),"queues":container.queue.stats_by_queue()}
    @router.get("/dead")
    async def dead_items(limit: int=Query(100,ge=1,le=1000),queue: str=""):return {"items":dead.list(limit,queue)}
    @router.post("/{task_id}/retry",dependencies=[Depends(auth.require)])
    async def retry(task_id: str):dead.replay(task_id);return {"id":task_id,"status":"pending"}
    @router.post("/{task_id}/cancel",dependencies=[Depends(auth.require)])
    async def cancel(task_id: str,reason: str="operator"):return {"id":task_id,"cancelled":container.queue.cancel(task_id,reason)}
    return router
