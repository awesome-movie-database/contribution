from contribution.domain import UserId
from contribution.infrastructure.database import PermissionsMapper
from contribution.infrastructure.cache import PermissionsCache


class PermissionsDoNotExistError(Exception):
    ...


class PermissionsStorage:
    def __init__(
        self,
        permissions_mapper: PermissionsMapper,
        permissions_cache: PermissionsCache,
    ):
        self._permissions_mapper = permissions_mapper
        self._permissions_cache = permissions_cache

    async def get(self, user_id: UserId) -> int:
        permissions_from_cache = await self._permissions_cache.get(user_id)
        if permissions_from_cache:
            return permissions_from_cache

        permissions_from_database = await self._permissions_mapper.get(user_id)
        if not permissions_from_database:
            raise PermissionsDoNotExistError()

        await self._permissions_cache.save(
            user_id=user_id,
            permissions=permissions_from_database,
        )

        return permissions_from_database

    async def save(self, user_id: UserId, permissions: int) -> None:
        await self._permissions_mapper.save(
            user_id=user_id,
            permissions=permissions,
        )
        await self._permissions_cache.save(
            user_id=user_id,
            permissions=permissions,
        )
