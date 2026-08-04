from catalog.image_pipeline import shopify_files

def test_image_pipeline_builds_shopify_file_inputs():
    files=shopify_files(["https://cdn.example/a.jpg","invalid"],"Widget")
    assert files==[{"originalSource":"https://cdn.example/a.jpg","alt":"Widget — image 1","contentType":"IMAGE"}]
