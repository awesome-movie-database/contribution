from typing import Optional

from contribution.domain.value_objects import AchievementId
from contribution.application.common.exceptions import (
    AchievementDoesNotExistError,
)
from contribution.application.common.gateways import AchievementGateway
from contribution.application.common.callbacks import OnAchievementEarned
from .command import CommandProcessor


class AchievementEearnedCallbackProcessor[C]:
    def __init__(
        self,
        *,
        processor: CommandProcessor[C, Optional[AchievementId]],
        achievement_gateway: AchievementGateway,
        on_achievement_earned: OnAchievementEarned,
    ):
        self._processor = processor
        self._achievement_gateway = achievement_gateway
        self._on_achievement_earned = on_achievement_earned

    async def process(self, command: C) -> Optional[AchievementId]:
        result = await self._processor.process(command)

        if not result:
            return result

        achievement = await self._achievement_gateway.with_id(result)
        if not achievement:
            raise AchievementDoesNotExistError()

        await self._on_achievement_earned(
            id=achievement.id,
            user_id=achievement.user_id,
            achieved=achievement.achieved,
            achieved_at=achievement.achieved_at,
        )

        return result
