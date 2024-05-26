from typing import Protocol, Optional

from contribution.domain import AchievementId, Achievement


class AchievementGateway(Protocol):
    async def by_id(self, id: AchievementId) -> Optional[Achievement]:
        raise NotImplementedError

    async def save(self, achievement: Achievement) -> None:
        raise NotImplementedError
