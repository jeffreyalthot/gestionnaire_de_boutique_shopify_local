class ShopifyAPIError(RuntimeError):
    def __init__(self, message: str, errors: list[dict[str, object]] | None = None) -> None:
        super().__init__(message)
        self.errors = errors or []

def raise_for_graphql_errors(payload: dict[str, object]) -> None:
    errors = payload.get("errors")
    if isinstance(errors, list) and errors:
        raise ShopifyAPIError("Erreur GraphQL Shopify", errors)
