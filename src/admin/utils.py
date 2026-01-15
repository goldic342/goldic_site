from urllib.parse import urlparse
from admin.config import admin_settings
import os
import time
from fastapi import Request, HTTPException


_bucket: list[float] = []


def url_to_meta(url: str) -> dict:
    path = urlparse(url).path
    return {"name": os.path.basename(path), "url": url}


async def rate_limit(_: Request):
    now = time.time()
    cutoff = now - admin_settings.WINDOW

    _bucket[:] = [t for t in _bucket if t > cutoff]

    if len(_bucket) >= admin_settings.MAX_REQS:
        raise HTTPException(status_code=429, detail="Stop it!")

    _bucket.append(now)
