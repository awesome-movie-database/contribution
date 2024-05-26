from typing import Optional

from contribution.domain import AchievementId
from contribution.application.common.exceptions import (
    AchievementDoesNotExistError,
)
from contribution.application.common.gateways import AchievementGateway
from contribution.application.common.event_callback import OnEventOccurred
from contribution.application.common.events import AchievementEarnedEvent
from .command import CommandProcessor


class AchievementEearnedCallbackProcessor[C]:
    def __init__(
        self,
        *,
        processor: CommandProcessor[C, Optional[AchievementId]],
        achievement_gateway: AchievementGateway,
        on_achievement_earned: OnEventOccurred[AchievementEarnedEvent],
    ):
        self._processor = processor
        self._achievement_gateway = achievement_gateway
        self._on_achievement_earned = on_achievement_earned

    async def process(self, command: C) -> Optional[AchievementId]:
        result = await self._processor.process(command)

        if not result:
            return result

        achievement = await self._achievement_gateway.by_id(result)
        if not achievement:
            raise AchievementDoesNotExistError()

        event = AchievementEarnedEvent(
            achievement_id=achievement.id,
            user_id=achievement.user_id,
            achieved=achievement.achieved,
            achieved_at=achievement.achieved_at,
        )
        await self._on_achievement_earned(event)

        return result
