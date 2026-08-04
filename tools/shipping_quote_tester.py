import asyncio,json
from app.bootstrap import bootstrap
async def run(product_id: str,sku_id: str,country: str,postal: str,quantity: int=1):
    app=bootstrap()
    try: return await app.container.alibaba.calculate_product_freight(product_id,sku_id,quantity,country,postal)
    finally: await app.container.close()
