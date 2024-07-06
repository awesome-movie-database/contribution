from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import UserId
from contribution.infrastructure.database.collections import (
    PermissionsCollection,
)


class PermissionsMapper:
    def __init__(
        self,
        permissions_collection: PermissionsCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._permissions_collection = permissions_collection
        self._session = session

    async def get(self, user_id: UserId) -> Optional[int]:
        document = await self._permissions_collection.find_one(
            {"user_id": user_id.hex},
            session=self._session,
        )
        if document:
            permissions = document["permissions"]
            return permissions

        return None

    async def save(self, user_id: UserId, permissions: int) -> None:
        document = {"user_id": user_id.hex, "permissions": permissions}
        await self._permissions_collection.insert_one(document)
        await self._session.commit_transaction()
