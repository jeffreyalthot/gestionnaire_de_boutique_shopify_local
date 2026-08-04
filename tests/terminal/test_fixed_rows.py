import pytest
from dashboard.fixed_line_registry import FixedLineRegistry

def test_fixed_rows_are_unique_and_sorted():
    rows=FixedLineRegistry(80); rows.register("b",2); rows.register("a",1)
    assert [line.row for line in rows.rows()]==[1,2]
    with pytest.raises(ValueError): rows.register("collision",2)
