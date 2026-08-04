from __future__ import annotations

from pathlib import Path
from typing import Any


class ShopifyStagedUpload:
    CREATE_MUTATION = """mutation stagedUploadsCreate($input: [StagedUploadInput!]!) { stagedUploadsCreate(input: $input) { stagedTargets { url resourceUrl parameters { name value } } userErrors { field message } } }"""

    def __init__(self, transport: Any) -> None:
        self.transport = transport

    async def create_target(self, path: Path, content_type: str) -> dict[str, Any]:
        variables = {"input": [{"filename": path.name, "mimeType": content_type, "httpMethod": "POST", "resource": "IMAGE", "fileSize": str(path.stat().st_size)}]}
        data = await self.transport.execute(self.CREATE_MUTATION, variables)
        payload = data.get("stagedUploadsCreate", data)
        errors = payload.get("userErrors", [])
        if errors:
            raise ValueError(f"Shopify staged upload refusé: {errors}")
        targets = payload.get("stagedTargets", [])
        if not targets:
            raise ValueError("Shopify n'a retourné aucune cible staged upload")
        return targets[0]
