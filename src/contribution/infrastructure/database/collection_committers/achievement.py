from typing import Any, Sequence

from pymongo import InsertOne, UpdateOne, DeleteOne

from contribution.domain import Achievement
from contribution.infrastructure.database.collections import (
    AchievementCollection,
)


class CommitAchievementCollectionChanges:
    def __init__(self, collection: AchievementCollection):
        self._collection = collection

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
                {"id": clean_achievement.id},
                self._pipeline_to_update_achievement(
                    clean_achievement,
                    dirty_achievement,
                ),
            )
            for clean_achievement, dirty_achievement in zip(clean, dirty)
        ]
        deletes = [
            DeleteOne({"id": achievement.id}) for achievement in deleted
        ]

        changes: list[InsertOne, UpdateOne, DeleteOne] = [
            *inserts,
            *updates,
            *deletes,
        ]
        await self._collection.bulk_write(changes)

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
