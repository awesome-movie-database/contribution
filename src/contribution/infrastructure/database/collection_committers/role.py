from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import Role
from contribution.infrastructure.database.collections import (
    RoleCollection,
)


class CommitRoleCollectionChanges:
    def __init__(
        self,
        collection: RoleCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[Role],
        clean: Sequence[Role],
        dirty: Sequence[Role],
        deleted: Sequence[Role],
    ) -> None:
        inserts = [InsertOne(self._role_to_document(role)) for role in new]
        updates = [
            UpdateOne(
                {"id": clean_role.id.hex},
                self._pipeline_to_update_role(clean_role, dirty_role),
            )
            for clean_role, dirty_role in zip(clean, dirty)
        ]
        deletes = [DeleteOne({"id": role.id.hex}) for role in deleted]

        changes: list[InsertOne, UpdateOne, DeleteOne] = [
            *inserts,
            *updates,
            *deletes,
        ]
        if changes:
            await self._collection.bulk_write(
                requests=changes,
                session=self._session,
            )

    def _role_to_document(self, role: Role) -> dict[str, Any]:
        document = {
            "id": role.id.hex,
            "movie_id": role.movie_id.hex,
            "person_id": role.person_id.hex,
            "character": role.character,
            "importance": role.importance,
            "is_spoiler": role.is_spoiler,
        }
        return document

    def _pipeline_to_update_role(
        self,
        clean: Role,
        dirty: Role,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.character != dirty.character:
            pipeline["$set"]["character"] = dirty.character
        if clean.importance != dirty.importance:
            pipeline["$set"]["importance"] = dirty.importance
        if clean.is_spoiler != dirty.is_spoiler:
            pipeline["$set"]["is_spoiler"] = dirty.is_spoiler

        return pipeline
