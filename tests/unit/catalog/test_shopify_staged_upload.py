import pytest
from catalog.media.shopify_staged_upload import ShopifyStagedUpload

class RefusingTransport:
    async def execute(self,*args): return {"stagedUploadsCreate":{"stagedTargets":[],"userErrors":[{"message":"denied"}]}}

@pytest.mark.asyncio
async def test_staged_upload_surfaces_shopify_user_errors(tmp_path):
    path=tmp_path/"a.jpg"; path.write_bytes(b"x")
    with pytest.raises(ValueError,match="refusé"): await ShopifyStagedUpload(RefusingTransport()).create_target(path,"image/jpeg")
