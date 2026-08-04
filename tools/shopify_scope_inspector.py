import asyncio,json
from app.bootstrap import bootstrap
from integrations.shopify.scope_validator import ScopeValidator
REQUIRED={"read_products","write_products","read_orders","write_orders","read_inventory","write_inventory","read_fulfillments","write_fulfillments"}
async def run():
    app=bootstrap()
    try: return await ScopeValidator(app.container.shopify).validate(REQUIRED)
    finally: await app.container.close()
if __name__=="__main__": print(json.dumps(asyncio.run(run()),indent=2))
