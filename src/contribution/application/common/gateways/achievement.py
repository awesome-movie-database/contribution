from typing import Protocol

from contribution.domain.entities import Achievement


class AchievementGateway(Protocol):
    async def save(self, achievement: Achievement) -> None:
        raise NotImplementedError
