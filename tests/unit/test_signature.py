from integrations.alibaba.signer import AlibabaSigner
def test_sign_is_deterministic():
    signer=AlibabaSigner("secret","hmac")
    assert signer.sign({"b":2,"a":1})==signer.sign({"a":1,"b":2})
