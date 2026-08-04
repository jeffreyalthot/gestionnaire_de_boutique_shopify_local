class AlibabaAPIError(RuntimeError):
    def __init__(self,message: str,code: str="",payload: dict[str,object]|None=None) -> None:
        super().__init__(message); self.code=code; self.payload=payload or {}

def inspect_alibaba_response(payload: dict[str,object]) -> None:
    code=str(payload.get("error_code") or payload.get("code") or "")
    success=payload.get("success")
    if code or success is False:
        message=str(payload.get("msg") or payload.get("sub_msg") or payload.get("message") or "Erreur Alibaba")
        raise AlibabaAPIError(message,code,payload)
