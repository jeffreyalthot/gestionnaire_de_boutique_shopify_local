import pytest
from catalog.media.shopify_staged_upload import ShopifyStagedUpload

class Transport:
    async def execute(self,query,variables):
        assert variables["input"][0]["resource"]=="IMAGE"
        return {"stagedUploadsCreate":{"stagedTargets":[{"url":"https://upload.example","resourceUrl":"https://cdn.example/i.jpg","parameters":[]}],"userErrors":[]}}

@pytest.mark.asyncio
async def test_image_can_be_prepared_for_shopify(tmp_path):
    image=tmp_path/"image.jpg"; image.write_bytes(b"jpeg")
    target=await ShopifyStagedUpload(Transport()).create_target(image,"image/jpeg")
    assert target["resourceUrl"].endswith(".jpg")
