"""Examples for using the AliExpress adapter/gateway.

Run this script after setting the ALIEXPRESS_* variables in a .env file
or environment so that get_settings() sees valid values.
"""

from __future__ import annotations

import asyncio

from config.settings import get_settings
from integrations import get_supplier_client


async def main() -> None:
    settings = get_settings()
    client = get_supplier_client(settings)
    # Search for items — uses AliExpress when configured
    try:
        res = await client.search_distribution_products("wireless charger", page=1, page_size=5)
        print("Search result:\n", res)
    except Exception as exc:
        print("Error during search:", exc)


if __name__ == "__main__":
    asyncio.run(main())
