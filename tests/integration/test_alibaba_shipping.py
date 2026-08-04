from integrations.alibaba.mappers.shipping_mapper import map_shipping_quote
def test_shipping_mapping(): assert map_shipping_quote({"shippingCost":12})["amount"]==12
