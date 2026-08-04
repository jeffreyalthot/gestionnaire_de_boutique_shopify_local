from integrations.alibaba.signer import AlibabaSigner
def test_vector(secret: str,params: dict[str,object],method: str="hmac") -> str: return AlibabaSigner(secret,method).sign(params)
