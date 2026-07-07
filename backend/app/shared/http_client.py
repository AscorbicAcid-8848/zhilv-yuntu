from __future__ import annotations

import httpx

from app.config import AMAP_TIMEOUT_SECONDS


_shared_client: httpx.Client | None = None


def get_http_client() -> httpx.Client:
    global _shared_client
    if _shared_client is None or _shared_client.is_closed:
        _shared_client = httpx.Client(timeout=AMAP_TIMEOUT_SECONDS)
    return _shared_client


def close_http_client() -> None:
    global _shared_client
    if _shared_client is not None and not _shared_client.is_closed:
        _shared_client.close()
    _shared_client = None
