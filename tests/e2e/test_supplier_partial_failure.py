import pytest
from orders.supplier_line_mapper import SupplierLineMapper

def test_supplier_partial_failure_is_detected_before_purchase():
    valid={"supplier_id":"s1","supplier_product_id":"p1","quantity":1}
    invalid={"supplier_id":"s2","quantity":1}
    with pytest.raises(ValueError): SupplierLineMapper().group([valid,invalid])
