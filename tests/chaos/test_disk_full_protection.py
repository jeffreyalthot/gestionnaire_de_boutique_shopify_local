from infrastructure.filesystem.disk_budget import DiskBudget

def test_disk_budget_blocks_impossible_reserve(tmp_path):
    snapshot=DiskBudget(tmp_path,required_free_bytes=10**30).snapshot()
    assert not snapshot.ok and snapshot.free < snapshot.required_free
