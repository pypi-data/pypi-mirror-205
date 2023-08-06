from typing import Optional, Tuple

from redis.asyncio.client import AbstractRedis as AioRedis
from redis.asyncio import RedisCluster as AioRedisCluster


class RedisBackend(AioRedis):
    def __init__(self) -> None:
        super().__init__()
        self.redis = redis
        self.is_cluster = isinstance(redis, AioRedisCluster)

    async def get_with_ttl(self, key: str) -> Tuple[int, str]:
        async with self.redis.pipeline(transaction=not self.is_cluster) as pipe:
            return await pipe.ttl(key).get(key).execute()

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: Optional[int] = None) -> None:
        return await self.redis.set(key, value, ex=expire)

    async def clear(self, namespace: str = None, key: str = None):
        namespace = namespace or self.prefix
        if namespace:
            async for k in self.scan_iter(f"{namespace}:*"):
                await self.delete(k)
            return True
        elif key:
            return await self.delete(key) if key else None

    async def all(self, namespace: str = None) -> list:
        namespace = namespace or self.prefix
        if namespace:
            keys = []
            async for key in self.scan_iter(f"{namespace}:*"):
                keys.append(key.decode())
            return keys
