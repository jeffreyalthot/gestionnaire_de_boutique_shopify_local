from __future__ import annotations

import re
from dataclasses import dataclass

_GID = re.compile(r"^gid://shopify/(?P<resource>[A-Za-z][A-Za-z0-9_]*)/(?P<identifier>[^/?#]+)$")


@dataclass(frozen=True, slots=True)
class ShopifyGID:
    resource: str
    identifier: str

    @property
    def value(self) -> str:
        return f"gid://shopify/{self.resource}/{self.identifier}"


def to_gid(resource: str, numeric_id: int | str) -> str:
    resource_name = str(resource).strip()
    identifier = str(numeric_id).strip()
    if not resource_name or not identifier:
        raise ValueError("resource and identifier are required")
    if "/" in resource_name or "/" in identifier:
        raise ValueError("resource and identifier cannot contain slashes")
    return ShopifyGID(resource_name, identifier).value


def parse_gid(gid: str) -> ShopifyGID:
    match = _GID.match(str(gid).strip())
    if not match:
        raise ValueError(f"invalid Shopify GID: {gid}")
    return ShopifyGID(match.group("resource"), match.group("identifier"))


def gid_numeric_id(gid: str) -> str:
    return parse_gid(gid).identifier
