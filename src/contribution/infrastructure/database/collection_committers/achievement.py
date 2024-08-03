from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne
from motor.motor_asyncio import AsyncIOMotorClientSession

from contribution.domain import Achievement
from contribution.infrastructure.database.collections import (
    AchievementCollection,
)


class CommitAchievementCollectionChanges:
    def __init__(
        self,
        collection: AchievementCollection,
        session: AsyncIOMotorClientSession,
    ):
        self._collection = collection
        self._session = session

    async def __call__(
        self,
        *,
        new: Sequence[Achievement],
        clean: Sequence[Achievement],
        dirty: Sequence[Achievement],
        deleted: Sequence[Achievement],
    ) -> None:
        inserts = [
            InsertOne(self._achievement_to_document(achievement))
            for achievement in new
        ]
        updates = [
            UpdateOne(
                {"id": clean_achievement.id.hex},
                self._pipeline_to_update_achievement(
                    clean_achievement,
                    dirty_achievement,
                ),
            )
            for clean_achievement, dirty_achievement in zip(clean, dirty)
        ]
        deletes = [
            DeleteOne({"id": achievement.id.hex}) for achievement in deleted
        ]

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

    def _achievement_to_document(
        self,
        achievement: Achievement,
    ) -> dict[str, Any]:
        document = {
            "id": achievement.id.hex,
            "user_id": achievement.user_id.hex,
            "achieved": achievement.achieved,
            "achieved_at": achievement.achieved_at.isoformat(),
        }
        return document

    def _pipeline_to_update_achievement(
        self,
        clean: Achievement,
        dirty: Achievement,
    ) -> dict[str, Any]:
        pipeline = {"$set": {}}

        if clean.achieved != dirty.achieved:
            pipeline["$set"]["achieved"] = dirty.achieved
        if clean.achieved_at != dirty.achieved_at:
            pipeline["$set"]["achieved_at"] = dirty.achieved_at.isoformat()

        return pipeline
