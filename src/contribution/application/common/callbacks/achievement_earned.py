from typing import Protocol
from datetime import datetime

from contribution.domain.constants import Achieved
from contribution.domain.value_objects import (
    UserId,
    AchievementId,
)


class OnAchievementEarned(Protocol):
    async def __call__(
        self,
        *,
        id: AchievementId,
        user_id: UserId,
        achieved: Achieved,
        achieved_at: datetime,
    ):
        raise NotImplementedError
