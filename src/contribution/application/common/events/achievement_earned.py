from dataclasses import dataclass
from datetime import datetime

from contribution.domain.constants import Achieved
from contribution.domain.value_objects import (
    UserId,
    AchievementId,
)


@dataclass(frozen=True, slots=True)
class AchievementEarnedEvent:
    achievement_id: AchievementId
    user_id: UserId
    achieved: Achieved
    achieved_at: datetime
