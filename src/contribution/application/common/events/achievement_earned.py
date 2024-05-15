from dataclasses import dataclass
from datetime import datetime

from contribution.domain import (
    Achieved,
    UserId,
    AchievementId,
)


@dataclass(frozen=True, slots=True)
class AchievementEarnedEvent:
    achievement_id: AchievementId
    user_id: UserId
    achieved: Achieved
    achieved_at: datetime
