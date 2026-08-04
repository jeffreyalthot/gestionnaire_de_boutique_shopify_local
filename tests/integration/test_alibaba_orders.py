from integrations.alibaba.mappers.order_mapper import map_order
def test_order_mapping(): assert map_order({"orderId":7})["order_id"]=="7"
