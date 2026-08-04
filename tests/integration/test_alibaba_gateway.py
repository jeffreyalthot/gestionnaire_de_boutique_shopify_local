from integrations.alibaba.signer import AlibabaSigner
def test_alibaba_common_signing(): assert len(AlibabaSigner("secret").sign({"method":"x","app_key":"y"}))==32
