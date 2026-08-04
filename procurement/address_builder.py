from domain.value_objects.address import Address
def build_supplier_address(payload: dict[str,object]) -> dict[str,str]:
    address=Address(
        first_name=str(payload.get("firstName") or payload.get("first_name") or ""),
        last_name=str(payload.get("lastName") or payload.get("last_name") or ""),
        company=str(payload.get("company") or ""),
        address1=str(payload.get("address1") or ""),
        address2=str(payload.get("address2") or ""),
        city=str(payload.get("city") or ""),
        province=str(payload.get("province") or payload.get("provinceCode") or ""),
        country_code=str(payload.get("countryCodeV2") or payload.get("country_code") or ""),
        postal_code=str(payload.get("zip") or payload.get("postal_code") or ""),
        phone=str(payload.get("phone") or ""),
    )
    return address.as_supplier_payload()
