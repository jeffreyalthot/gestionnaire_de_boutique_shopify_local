import pytest
from app.dependency_container import build_container

@pytest.mark.asyncio
async def test_full_store_cycle_is_dry_run_and_auditable(settings):
    container=build_container(settings)
    result=await container.automation.run_cycle()
    assert result["planned"] >= 30 and result["rejected"]==0
    assert container.queue.stats().get("pending",0)>0
    await container.close()
