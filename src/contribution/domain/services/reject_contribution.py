from datetime import datetime
from typing import Optional

from contribution.domain.constants import (
    ContributionStatus,
    Achieved,
)
from contribution.domain.value_objects import AchievementId
from contribution.domain.entities import (
    Contribution,
    User,
    Achievement,
)

REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_1 = 1
REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_2 = 10
REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_3 = 100
REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_4 = 500
REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_5 = 1000
REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_6 = 10000

ACHIEVEMENTS = {
    REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_1: Achieved.REJECTED_CONTRIBUTIONS_1,
    REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_2: Achieved.REJECTED_CONTRIBUTIONS_2,
    REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_3: Achieved.REJECTED_CONTRIBUTIONS_3,
    REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_4: Achieved.REJECTED_CONTRIBUTIONS_4,
    REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_5: Achieved.REJECTED_CONTRIBUTIONS_5,
    REJECTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_6: Achieved.REJECTED_CONTRIBUTIONS_6,
}


class RejectContribution:
    def __call__(
        self,
        *,
        achievement_id: AchievementId,
        contribution: Contribution,
        author: User,
        current_timestamp: datetime,
    ) -> Optional[Achievement]:
        contribution.status = ContributionStatus.REJECTED
        contribution.status_updated_at = current_timestamp

        author.rejected_contributions_count += 1

        return self._try_earn_achievement(
            id=achievement_id,
            user=author,
            current_timestamp=current_timestamp,
        )

    def _try_earn_achievement(
        self,
        *,
        id: AchievementId,
        user: User,
        current_timestamp: datetime,
    ) -> Optional[Achievement]:
        achieved = ACHIEVEMENTS.get(
            user.rejected_contributions_count,
            None,
        )
        if achieved:
            return Achievement(
                id=id,
                user_id=user.id,
                achieved=achieved,
                achieved_at=current_timestamp,
            )
        return None
