from datetime import datetime

from contribution.domain.constants import ContributionStatus
from contribution.domain.entities import (
    Contribution,
    User,
)


class AcceptContribution:
    def __init__(self, increase_rating_on: float):
        self._increase_rating_on = increase_rating_on

    def __call__(
        self,
        *,
        contribution: Contribution,
        author: User,
        current_timestamp: datetime,
    ) -> None:
        contribution.status = ContributionStatus.ACCEPTED
        contribution.updated_at = current_timestamp

        author.rating += self._increase_rating_on
        author.contributions_count += 1
