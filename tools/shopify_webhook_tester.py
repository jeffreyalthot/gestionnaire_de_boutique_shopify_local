import base64,hashlib,hmac,json
def signed_headers(payload: dict[str,object],secret: str) -> tuple[bytes,dict[str,str]]:
    body=json.dumps(payload,separators=(",",":")).encode()
    signature=base64.b64encode(hmac.new(secret.encode(),body,hashlib.sha256).digest()).decode()
    return body,{"X-Shopify-Hmac-Sha256":signature,"X-Shopify-Webhook-Id":"local-test","X-Shopify-Topic":"orders/paid","X-Shopify-Shop-Domain":"test.myshopify.com"}
