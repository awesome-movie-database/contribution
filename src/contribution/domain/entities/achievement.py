from dataclasses import dataclass
from datetime import datetime

from contribution.domain.constants import Achieved
from contribution.domain.value_objects import (
    AchievementId,
    UserId,
)


@dataclass(slots=True)
class Achievement:
    id: AchievementId
    user_id: UserId
    achieved: Achieved
    achieved_at: datetime
