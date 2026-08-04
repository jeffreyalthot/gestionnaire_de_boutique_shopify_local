import asyncio,argparse,json
from app.bootstrap import bootstrap
async def run(method: str,params: dict[str,object]):
    app=bootstrap()
    try: return await app.container.alibaba_gateway.call(method,params)
    finally: await app.container.close()
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("method"); p.add_argument("--params",default="{}")
    a=p.parse_args(); print(json.dumps(asyncio.run(run(a.method,json.loads(a.params))),indent=2,default=str))
