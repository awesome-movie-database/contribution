from typing import Any, Sequence

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import InsertOne, UpdateOne, DeleteOne

from contribution.domain import User


class CommitUserCollectionChanges:
    def __init__(self, user_collection: AsyncIOMotorCollection):
        self._collection = user_collection

    async def __call__(
        self,
        *,
        new: Sequence[User],
        clean: Sequence[User],
        dirty: Sequence[User],
        deleted: Sequence[User],
    ) -> None:
        inserts = [InsertOne(self._user_to_document(user)) for user in new]
        updates = [
            UpdateOne(
                {"id": clean_user.id},
                self._pipeline_to_update_user(clean_user, dirty_user),
            )
            for clean_user, dirty_user in zip(clean, dirty)
        ]
        deletes = [DeleteOne({"id": user.id}) for user in deleted]

        changes = [*inserts, *updates, *deletes]
        await self._collection.bulk_write(changes)

    def _user_to_document(self, user: User) -> dict[str, Any]:
        document = {
            "id": user.id.hex,
            "name": user.name,
            "is_active": user.is_active,
            "rating": user.rating,
            "accepted_contributions_count": (
                user.accepted_contributions_count
            ),
            "rejected_contributions_count": (
                user.rejected_contributions_count
            ),
        }

        if user.email:
            document["email"] = user.email.value
        else:
            document["email"] = None

        if user.telegram:
            document["telegram"] = user.telegram.value
        else:
            document["telegram"] = None

        return document

    def _pipeline_to_update_user(
        self,
        clean: User,
        dirty: User,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.name != dirty.name:
            pipeline["$set"]["name"] = dirty.name
        if clean.email != dirty.email:
            if dirty.email:
                pipeline["$set"]["email"] = dirty.email.value
            else:
                pipeline["$set"]["email"] = None
        if clean.telegram != dirty.telegram:
            if dirty.telegram:
                pipeline["$set"]["telegram"] = dirty.telegram.value
            else:
                pipeline["$set"]["telegram"] = None
        if clean.is_active != dirty.is_active:
            pipeline["$set"]["is_active"] = dirty.is_active
        if clean.rating != dirty.rating:
            pipeline["$set"]["rating"] = dirty.rating
        if (
            clean.accepted_contributions_count
            != dirty.accepted_contributions_count
        ):
            pipeline["$set"][
                "accepted_contributions_count"
            ] = dirty.accepted_contributions_count
        if (
            clean.rejected_contributions_count
            != dirty.rejected_contributions_count
        ):
            pipeline["$set"][
                "rejected_contributions_count"
            ] = dirty.rejected_contributions_count

        return pipeline
