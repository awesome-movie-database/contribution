from datetime import datetime

from contribution.domain.constants import ContributionStatus
from contribution.domain.entities import (
    Contribution,
    User,
)


class RejectContribution:
    def __call__(
        self,
        *,
        contribution: Contribution,
        author: User,
        current_timestamp: datetime,
    ) -> None:
        contribution.status = ContributionStatus.REJECTED
        contribution.updated_at = current_timestamp

        author.rejected_contributions_count += 1
