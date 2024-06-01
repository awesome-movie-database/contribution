from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from contribution.domain import (
    Achieved,
    AchievementId,
    UserId,
    Achievement,
)
from contribution.infrastructure.database.identity_maps import (
    AchievementMap,
)
from contribution.infrastructure.database.lock_factory import (
    MongoDBLockFactory,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class AchievementMapper:
    def __init__(
        self,
        achievement_map: AchievementMap,
        collection: AsyncIOMotorCollection,
        lock_factory: MongoDBLockFactory,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._achievement_map = achievement_map
        self._collection = collection
        self._lock_factory = lock_factory
        self._unit_of_work = unit_of_work

    async def by_id(self, id: AchievementId) -> Optional[Achievement]:
        achievement_from_map = self._achievement_map.by_id(id)
        if achievement_from_map:
            return achievement_from_map

        document_or_none = await self._collection.find_one(
            {"id": id.hex},
        )
        if document_or_none:
            achievement = self._document_to_achievement(document_or_none)
            self._achievement_map.save(achievement)
            self._unit_of_work.register_clean(achievement)
            return achievement

        return None

    async def save(self, achievement: Achievement) -> None:
        self._achievement_map.save(achievement)
        self._unit_of_work.register_clean(achievement)

    def _document_to_achievement(
        self,
        document: dict[str, Any],
    ) -> Achievement:
        return Achievement(
            id=AchievementId(UUID(document["id"])),
            user_id=UserId(UUID(document["user_id"])),
            achieved=Achieved(document["achieved"]),
            achieved_at=datetime.fromisoformat(document["achieved_at"]),
        )
