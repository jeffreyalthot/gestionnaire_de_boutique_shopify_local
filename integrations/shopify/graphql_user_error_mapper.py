from dataclasses import dataclass
@dataclass(frozen=True)
class ShopifyUserError:
    field: tuple[str,...]; message: str; code: str=''
def map_user_errors(node: dict)->tuple[ShopifyUserError, ...]:
    return tuple(ShopifyUserError(tuple(str(v) for v in item.get('field') or ()),str(item.get('message','Erreur')),str(item.get('code') or '')) for item in node.get('userErrors') or ())
