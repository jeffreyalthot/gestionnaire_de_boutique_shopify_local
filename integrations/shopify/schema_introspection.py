from integrations.shopify.graphql_transport import ShopifyGraphQLTransport
async def introspect_type(transport: ShopifyGraphQLTransport,name: str) -> dict[str,object] | None:
    data=await transport.execute("query Type($name:String!){__type(name:$name){name kind fields{name args{name type{kind name}}}}}",{"name":name})
    return data.get("__type")
