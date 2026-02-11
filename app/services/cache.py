import json
import os
from redis.asyncio import Redis
from redis.exceptions import RedisError

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
except Exception:
    redis_client = None


async def cache_get(key: str):
    if not redis_client:
        return None
    try:
        return await redis_client.get(key)
    except RedisError:
        return None


async def cache_set(key: str, value, ttl: int = 60):
    if not redis_client:
        return
    try:
        await redis_client.set(key, json.dumps(value), ex=ttl)
    except RedisError:
        pass


def cache_key(prefix: str, org_id: int, skip: int, limit: int):
    return f"{prefix}:org={org_id}:skip={skip}:limit={limit}"
