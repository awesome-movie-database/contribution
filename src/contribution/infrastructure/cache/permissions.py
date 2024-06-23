from typing import Optional

from redis.asyncio import Redis

from contribution.domain import UserId


HASH_MAP_KEY = "permissions"


class PermissionsCache:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get(self, user_id: UserId) -> Optional[int]:
        permissions = await self._redis.hget(
            name=HASH_MAP_KEY,
            key=self._key_factory(user_id),
        )
        if permissions:
            permissions = int(permissions)

        return permissions

    async def save(self, user_id: UserId, permissions: int) -> None:
        await self._redis.hset(
            name=HASH_MAP_KEY,
            key=self._key_factory(user_id),
            value=str(permissions),
        )

    def _key_factory(self, user_id: UserId) -> str:
        return f"user_id:{user_id.hex}"
