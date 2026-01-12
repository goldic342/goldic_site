from urllib.parse import urlparse
import os


def url_to_meta(url: str) -> dict:
    path = urlparse(url).path
    return {"name": os.path.basename(path), "url": url}
