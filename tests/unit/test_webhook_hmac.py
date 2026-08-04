import base64,hashlib,hmac
from security.webhook_security import verify_shopify_hmac
def test_shopify_hmac():
    body=b'{"id":1}'; secret="abc"
    sig=base64.b64encode(hmac.new(secret.encode(),body,hashlib.sha256).digest()).decode()
    assert verify_shopify_hmac(body,sig,secret)
