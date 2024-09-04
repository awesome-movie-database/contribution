from datetime import datetime
from typing import Optional

from contribution.domain.constants import (
    ContributionStatus,
    Achieved,
)
from contribution.domain.value_objects import AchievementId
from contribution.domain.models import (
    Contribution,
    User,
    Achievement,
)


INCREASE_RATING_ON = 10

ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_1 = 1
ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_2 = 10
ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_3 = 100
ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_4 = 500
ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_5 = 1000
ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_6 = 10000

ACHIEVEMENTS = {
    ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_1: Achieved.ACCEPTED_CONTRIBUTIONS_1,
    ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_2: Achieved.ACCEPTED_CONTRIBUTIONS_2,
    ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_3: Achieved.ACCEPTED_CONTRIBUTIONS_3,
    ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_4: Achieved.ACCEPTED_CONTRIBUTIONS_4,
    ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_5: Achieved.ACCEPTED_CONTRIBUTIONS_5,
    ACCEPTED_CONTRIBUTIONS_FOR_ACHIEVEMENT_6: Achieved.ACCEPTED_CONTRIBUTIONS_6,
}


class AcceptContribution:
    def __call__(
        self,
        *,
        achievement_id: AchievementId,
        contribution: Contribution,
        author: User,
        current_timestamp: datetime,
    ) -> Optional[Achievement]:
        contribution.status = ContributionStatus.ACCEPTED
        contribution.status_updated_at = current_timestamp

        author.rating += INCREASE_RATING_ON
        author.accepted_contributions_count += 1

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
            user.accepted_contributions_count,
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
