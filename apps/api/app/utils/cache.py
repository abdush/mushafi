import hashlib
import json
from typing import Any

from app.core.config import settings
from app.core.redis import get_redis


def _make_key(prefix: str, **params) -> str:
    params_hash = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()[:8]
    return f"qf:{prefix}:{params_hash}"


async def cache_get(key: str) -> Any | None:
    redis = await get_redis()
    value = await redis.get(key)
    if value:
        return json.loads(value)
    return None


async def cache_set(key: str, value: Any, ttl: int = settings.redis_cache_ttl) -> None:
    redis = await get_redis()
    await redis.setex(key, ttl, json.dumps(value))


async def cache_delete(key: str) -> None:
    redis = await get_redis()
    await redis.delete(key)
