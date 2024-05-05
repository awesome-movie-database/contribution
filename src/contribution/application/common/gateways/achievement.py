from typing import Protocol, Optional

from contribution.domain.value_objects import AchievementId
from contribution.domain.entities import Achievement


class AchievementGateway(Protocol):
    async def with_id(self, id: AchievementId) -> Optional[Achievement]:
        raise NotImplementedError

    async def save(self, achievement: Achievement) -> None:
        raise NotImplementedError
