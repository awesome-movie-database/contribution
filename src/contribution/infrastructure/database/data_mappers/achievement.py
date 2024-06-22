from datetime import datetime
from typing import Any, Mapping, Optional
from uuid import UUID

from contribution.domain import (
    Achieved,
    AchievementId,
    UserId,
    Achievement,
)
from contribution.infrastructure.database.collections import (
    AchievementCollection,
)
from contribution.infrastructure.database.identity_maps import (
    AchievementMap,
)
from contribution.infrastructure.database.unit_of_work import (
    MongoDBUnitOfWork,
)


class AchievementMapper:
    def __init__(
        self,
        achievement_map: AchievementMap,
        achievement_collection: AchievementCollection,
        unit_of_work: MongoDBUnitOfWork,
    ):
        self._achievement_map = achievement_map
        self._achievement_collection = achievement_collection
        self._unit_of_work = unit_of_work

    async def by_id(self, id: AchievementId) -> Optional[Achievement]:
        achievement_from_map = self._achievement_map.by_id(id)
        if achievement_from_map:
            return achievement_from_map

        document = await self._achievement_collection.find_one(
            {"id": id.hex},
        )
        if document:
            achievement = self._document_to_achievement(document)
            self._achievement_map.save(achievement)
            self._unit_of_work.register_clean(achievement)
            return achievement

        return None

    async def save(self, achievement: Achievement) -> None:
        self._achievement_map.save(achievement)
        self._unit_of_work.register_clean(achievement)

    def _document_to_achievement(
        self,
        document: Mapping[str, Any],
    ) -> Achievement:
        return Achievement(
            id=AchievementId(UUID(document["id"])),
            user_id=UserId(UUID(document["user_id"])),
            achieved=Achieved(document["achieved"]),
            achieved_at=datetime.fromisoformat(document["achieved_at"]),
        )
