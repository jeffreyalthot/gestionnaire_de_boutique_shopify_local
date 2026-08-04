from __future__ import annotations
from typing import Any
from integrations.shopify.graphql_transport import ShopifyGraphQLTransport
from integrations.shopify.error_mapper import ShopifyAPIError

class ShopifyClient:
    def __init__(self, transport: ShopifyGraphQLTransport) -> None:
        self.transport=transport

    @staticmethod
    def _user_errors(node: dict[str, Any], operation: str) -> None:
        errors=node.get("userErrors") or []
        if errors:
            messages="; ".join(str(e.get("message","Erreur")) for e in errors)
            raise ShopifyAPIError(f"{operation}: {messages}", errors)

    async def shop(self) -> dict[str, Any]:
        data=await self.transport.execute("""
        query ShopIdentity {
          shop { id name email currencyCode myshopifyDomain primaryDomain { url } }
        }""")
        return data["shop"]

    async def current_app_installation(self) -> dict[str, Any]:
        data=await self.transport.execute("""
        query Installation {
          currentAppInstallation { id accessScopes { handle } }
        }""")
        return data["currentAppInstallation"]

    async def products(self, first: int=50, after: str | None=None, query_filter: str="") -> dict[str, Any]:
        data=await self.transport.execute("""
        query Products($first:Int!,$after:String,$query:String) {
          products(first:$first,after:$after,query:$query) {
            edges { cursor node {
              id title handle status vendor productType tags
              featuredMedia { preview { image { url altText width height } } }
              variants(first:100) { nodes {
                id title sku barcode price inventoryQuantity
                selectedOptions { name value }
                inventoryItem { id tracked unitCost { amount currencyCode } }
              }}
            }}
            pageInfo { hasNextPage endCursor }
          }
        }""",{"first":first,"after":after,"query":query_filter or None})
        return data["products"]

    async def product_by_id(self, product_id: str) -> dict[str, Any] | None:
        data=await self.transport.execute("""
        query Product($id:ID!){ product(id:$id){
          id title descriptionHtml handle status vendor productType tags
          media(first:50){nodes{... on MediaImage{id image{url altText width height}}}}
          variants(first:100){nodes{id title sku barcode price inventoryQuantity selectedOptions{name value}
            inventoryItem{id tracked unitCost{amount currencyCode}}}}
        }}""",{"id":product_id})
        return data.get("product")

    async def product_set(self, product_input: dict[str, Any], synchronous: bool=True) -> dict[str, Any]:
        data=await self.transport.execute("""
        mutation ProductSet($input:ProductSetInput!,$sync:Boolean!){
          productSet(input:$input,synchronous:$sync){
            product{id title status handle variants(first:100){nodes{id sku price inventoryQuantity}}}
            productSetOperation{id status userErrors{field message}}
            userErrors{field message code}
          }
        }""",{"input":product_input,"sync":synchronous})
        node=data["productSet"]; self._user_errors(node,"productSet")
        return node

    async def publish(self, product_id: str, publication_id: str) -> dict[str, Any]:
        data=await self.transport.execute("""
        mutation Publish($id:ID!,$publicationId:ID!){
          publishablePublish(id:$id,input:{publicationId:$publicationId}){
            publishable{publishedOnCurrentPublication}
            userErrors{field message}
          }
        }""",{"id":product_id,"publicationId":publication_id})
        node=data["publishablePublish"]; self._user_errors(node,"publishablePublish"); return node

    async def publications(self) -> list[dict[str, Any]]:
        data=await self.transport.execute("query Publications{publications(first:50){nodes{id name}}}")
        return data["publications"]["nodes"]

    async def orders(self, first: int=50, after: str | None=None, query_filter: str="") -> dict[str, Any]:
        data=await self.transport.execute("""
        query Orders($first:Int!,$after:String,$query:String){
          orders(first:$first,after:$after,query:$query,sortKey:UPDATED_AT,reverse:true){
            edges{cursor node{
              id name createdAt updatedAt displayFinancialStatus displayFulfillmentStatus
              currentTotalPriceSet{shopMoney{amount currencyCode}}
              totalShippingPriceSet{shopMoney{amount currencyCode}}
              customer{id email firstName lastName}
              shippingAddress{firstName lastName company address1 address2 city province provinceCode
                country countryCodeV2 zip phone}
              lineItems(first:250){nodes{id name title sku quantity currentQuantity
                originalUnitPriceSet{shopMoney{amount currencyCode}}
                variant{id sku product{id} inventoryItem{id}}}}
              transactions{status kind gateway amountSet{shopMoney{amount currencyCode}}}
              fulfillments{id status trackingInfo{company number url}}
            }}
            pageInfo{hasNextPage endCursor}
          }
        }""",{"first":first,"after":after,"query":query_filter or None})
        return data["orders"]

    async def order(self, order_id: str) -> dict[str, Any] | None:
        data=await self.transport.execute("""
        query Order($id:ID!){order(id:$id){
          id name createdAt updatedAt displayFinancialStatus displayFulfillmentStatus
          currentTotalPriceSet{shopMoney{amount currencyCode}}
          totalShippingPriceSet{shopMoney{amount currencyCode}}
          customer{id email firstName lastName}
          shippingAddress{firstName lastName company address1 address2 city province provinceCode country countryCodeV2 zip phone}
          lineItems(first:250){nodes{id name title sku quantity currentQuantity originalUnitPriceSet{shopMoney{amount currencyCode}}
            variant{id sku product{id} inventoryItem{id}}}}
          fulfillments{id status trackingInfo{company number url}}
        }}""",{"id":order_id})
        return data.get("order")

    async def inventory_set(self, name: str, reason: str, quantities: list[dict[str, Any]]) -> dict[str, Any]:
        data=await self.transport.execute("""
        mutation InventorySet($input:InventorySetQuantitiesInput!){
          inventorySetQuantities(input:$input){
            inventoryAdjustmentGroup{createdAt reason changes{name delta quantityAfterChange}}
            userErrors{field message code}
          }
        }""",{"input":{"name":name,"reason":reason,"quantities":quantities,
                       "ignoreCompareQuantity":False}})
        node=data["inventorySetQuantities"]; self._user_errors(node,"inventorySetQuantities"); return node

    async def fulfillment_orders(self, order_id: str) -> list[dict[str, Any]]:
        data=await self.transport.execute("""
        query FulfillmentOrders($id:ID!){order(id:$id){fulfillmentOrders(first:100){nodes{
          id status requestStatus assignedLocation{location{id name}}
          lineItems(first:250){nodes{id remainingQuantity lineItem{id sku}}}
        }}}}""",{"id":order_id})
        return data.get("order",{}).get("fulfillmentOrders",{}).get("nodes",[])

    async def create_fulfillment(self, fulfillment_order_id: str, tracking: dict[str, Any],
                                 notify_customer: bool=True) -> dict[str, Any]:
        data=await self.transport.execute("""
        mutation Fulfill($fulfillment:FulfillmentV2Input!,$message:String){
          fulfillmentCreateV2(fulfillment:$fulfillment,message:$message){
            fulfillment{id status trackingInfo{company number url}}
            userErrors{field message}
          }
        }""",{"fulfillment":{"notifyCustomer":notify_customer,"trackingInfo":tracking,
                              "lineItemsByFulfillmentOrder":[{"fulfillmentOrderId":fulfillment_order_id}]},
                 "message":"Votre commande a été expédiée par notre fournisseur."})
        node=data["fulfillmentCreateV2"]; self._user_errors(node,"fulfillmentCreateV2"); return node

    async def update_tracking(self, fulfillment_id: str, tracking: dict[str, Any],
                              notify_customer: bool=True) -> dict[str, Any]:
        data=await self.transport.execute("""
        mutation Tracking($id:ID!,$input:FulfillmentTrackingInput!,$notify:Boolean!){
          fulfillmentTrackingInfoUpdateV2(fulfillmentId:$id,trackingInfoInput:$input,notifyCustomer:$notify){
            fulfillment{id status trackingInfo{company number url}}
            userErrors{field message}
          }
        }""",{"id":fulfillment_id,"input":tracking,"notify":notify_customer})
        node=data["fulfillmentTrackingInfoUpdateV2"]; self._user_errors(node,"fulfillmentTrackingInfoUpdateV2"); return node

    async def webhooks(self) -> list[dict[str, Any]]:
        data=await self.transport.execute("query Webhooks{webhookSubscriptions(first:250){nodes{id topic uri}}}")
        return data["webhookSubscriptions"]["nodes"]

    async def create_webhook(self, topic: str, uri: str) -> dict[str, Any]:
        data=await self.transport.execute("""
        mutation Hook($topic:WebhookSubscriptionTopic!,$sub:WebhookSubscriptionInput!){
          webhookSubscriptionCreate(topic:$topic,webhookSubscription:$sub){
            webhookSubscription{id topic uri}
            userErrors{field message}
          }
        }""",{"topic":topic,"sub":{"uri":uri,"format":"JSON"}})
        node=data["webhookSubscriptionCreate"]; self._user_errors(node,"webhookSubscriptionCreate"); return node

    async def bulk_query(self, query: str) -> dict[str, Any]:
        data=await self.transport.execute("""
        mutation Bulk($query:String!){
          bulkOperationRunQuery(query:$query){
            bulkOperation{id status type}
            userErrors{field message}
          }
        }""",{"query":query})
        node=data["bulkOperationRunQuery"]; self._user_errors(node,"bulkOperationRunQuery"); return node
