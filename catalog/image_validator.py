from urllib.parse import urlparse
def valid_image_urls(urls: list[str],maximum: int=20) -> list[str]:
    result=[]
    for url in urls:
        parsed=urlparse(str(url))
        if parsed.scheme=="https" and parsed.netloc and url not in result: result.append(url)
    return result[:maximum]
