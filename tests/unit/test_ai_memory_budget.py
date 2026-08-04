from ai.runtime.memory_budget import MemoryBudget
def test_memory_budget_snapshot(): assert MemoryBudget(750).snapshot().limit_mb==750
