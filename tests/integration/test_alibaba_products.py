from integrations.alibaba.mappers.product_mapper import map_alibaba_product
def test_product_mapping(): assert map_alibaba_product({"productId":1,"title":"A","price":"2"})["product_id"]=="1"
