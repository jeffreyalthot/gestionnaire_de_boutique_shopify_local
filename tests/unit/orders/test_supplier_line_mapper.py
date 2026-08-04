from orders.supplier_line_mapper import SupplierLineMapper

def test_supplier_lines_are_grouped_without_losing_quantity():
    groups=SupplierLineMapper().group([{"supplier_id":"s1","supplier_product_id":"p1","quantity":2},{"supplier_id":"s1","supplier_product_id":"p2","quantity":3}])
    assert len(groups)==1 and sum(line["quantity"] for line in groups["s1"])==5
