REQUIRED=[
"alibaba.icbu.distribution.product.query","alibaba.dropshipping.product.get","alibaba.icbu.product.sku.inventory.get",
"alibaba.shipping.freight.calculate","alibaba.order.freight.calculate","alibaba.buynow.order.create",
"alibaba.dropshipping.order.pay","alibaba.order.pay.result.query","alibaba.order.logistics.tracking.get",
"taobao.tmc.messages.consume","taobao.tmc.messages.confirm"]
if __name__=="__main__":
    print("Méthodes à demander dans Alibaba Open Platform:")
    for method in REQUIRED: print("-",method)
