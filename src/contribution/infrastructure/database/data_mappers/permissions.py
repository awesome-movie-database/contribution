from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import UserId
from contribution.infrastructure.database.collections import (
    PermissionsCollection,
)


class PermissionsMapper:
    def __init__(
        self,
        collection: PermissionsCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def get(self, user_id: UserId) -> Optional[int]:
        document = await self._collection.find_one(
            {"user_id": user_id.hex},
        )
        if document:
            permissions = document["permissions"]
            return permissions

        return None

    async def save(self, user_id: UserId, permissions: int) -> None:
        document = {"user_id": user_id.hex, "permissions": permissions}
        await self._collection.insert_one(document)
        await self._session.commit_transaction()
