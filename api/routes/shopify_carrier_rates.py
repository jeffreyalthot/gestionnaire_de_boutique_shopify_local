from fastapi import APIRouter,Request
def router_for():
    router=APIRouter()
    @router.post("/carrier-service/rates")
    async def rates(request: Request):
        payload=await request.json()
        return {"rates":[],"request_received":bool(payload)}
    return router
