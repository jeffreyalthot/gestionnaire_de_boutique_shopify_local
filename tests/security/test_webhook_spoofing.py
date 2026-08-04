from security.webhook_security import verify_shopify_hmac
def test_fake_signature_rejected(): assert not verify_shopify_hmac(b"{}", "fake", "secret")
