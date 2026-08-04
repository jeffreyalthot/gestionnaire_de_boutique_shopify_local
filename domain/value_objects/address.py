from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Address:
    first_name: str
    last_name: str
    address1: str
    city: str
    province: str
    country_code: str
    postal_code: str
    phone: str = ""
    address2: str = ""
    company: str = ""

    def validate(self) -> None:
        required = (self.first_name, self.last_name, self.address1, self.city, self.country_code, self.postal_code)
        if not all(value.strip() for value in required):
            raise ValueError("L'adresse est incomplète.")
        if len(self.country_code) != 2:
            raise ValueError("Le code pays doit contenir deux caractères.")

    def as_supplier_payload(self) -> dict[str, str]:
        self.validate()
        return {
            "firstName": self.first_name, "lastName": self.last_name, "address1": self.address1,
            "address2": self.address2, "city": self.city, "province": self.province,
            "countryCode": self.country_code.upper(), "postalCode": self.postal_code,
            "phone": self.phone, "company": self.company,
        }
