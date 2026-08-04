from decimal import Decimal
from integrations.currency.static_rate_provider import StaticRateProvider
import pytest
@pytest.mark.asyncio
async def test_currency(): assert await StaticRateProvider().rate("CAD","CAD")==Decimal("1")
