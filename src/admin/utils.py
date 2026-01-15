from urllib.parse import urlparse
from admin.config import admin_settings
import os
import time
from fastapi import Request, HTTPException


def url_to_meta(url: str) -> dict:
    path = urlparse(url).path
    return {"name": os.path.basename(path), "url": url}


_bucket: dict[str, list[float]] = {}


async def rate_limit(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.time()

    timestamps = _bucket.get(ip, [])
    timestamps = [t for t in timestamps if now - t < admin_settings.WINDOW]

    if len(timestamps) >= admin_settings.MAX_REQS:
        raise HTTPException(status_code=429, detail="rate limit exceeded")

    timestamps.append(now)
    _bucket[ip] = timestamps
